#!/usr/bin/env python3
"""Deterministic, mount-safe writer for the OPT-IN save path of document-mind-map.

WHY: the skill runs in-chat by default (ephemeral, lean). Only when Nile says "save this"
do we write to the vault — and that write must not silently lose data on the rclone Drive
mount. This mirrors transcribe-to-kb/emit_note.py: it owns the mount-liveness check, the
collision-safe filename, house frontmatter, idempotency, and the atomic write + read-back.
The model supplies only judgment (title, summary, the map body, tags, related links).

Emits one JSON line: {"result": WROTE|EXISTS|MOUNT_DOWN|ERROR, "path","filename","message"}.
Exit 0 on WROTE/EXISTS; 2 on MOUNT_DOWN; 3 on ERROR.
"""
import argparse, json, hashlib, os, re, sys, unicodedata, tempfile, datetime

HOUSE_ORDER = ["title", "tags", "type", "status", "summary", "created", "updated", "related", "aliases"]


def slugify(text, fallback):
    text = unicodedata.normalize("NFKD", text or "")
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    text = re.sub(r"-{2,}", "-", text)
    if len(text) > 60:
        text = text[:60].rsplit("-", 1)[0] or text[:60]
    return text or fallback


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--vault", required=True)               # resolved vault root (KB/Wellness/1,420…)
    ap.add_argument("--subdir", default="Mind Maps")
    ap.add_argument("--source", required=True)              # original path/url, or "pasted"
    ap.add_argument("--title", required=True)
    ap.add_argument("--summary", required=True)
    ap.add_argument("--body", required=True)                # the mind-map markdown (outline [+ mermaid])
    ap.add_argument("--tags", default="")                   # comma-sep
    ap.add_argument("--related", default="")               # comma-sep [[wikilink]] targets (no brackets)
    ap.add_argument("--source-date", required=True)         # STABLE date YYYY-MM-DD (source mtime/date), never "today"
    ap.add_argument("--capture-date", default=datetime.date.today().isoformat())
    a = ap.parse_args()

    def out(result, path="", filename="", code=0, msg=""):
        print(json.dumps({"result": result, "path": path, "filename": filename, "message": msg}))
        sys.exit(code)

    # Mount liveness: a dropped rclone FUSE mount reverts to an EMPTY local dir. Writing there
    # loses the map to local disk where Nile never finds it — refuse.
    if not os.path.isdir(a.vault) or not os.listdir(a.vault):
        out("MOUNT_DOWN", code=2, msg=f"vault missing/empty (mount down?): {a.vault}")

    # Collision-safe filename: hash of the source identity (or the body, for pasted docs with
    # no stable source) guarantees two different docs never share a filename; same source →
    # same filename → idempotent skip.
    ident = a.source if a.source.strip().lower() != "pasted" else a.body
    shash = hashlib.sha1(ident.encode("utf-8")).hexdigest()[:8]
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", a.source_date):
        a.source_date = a.capture_date  # stable fallback; never a silently-shifting run date beyond this
    slug = slugify(a.title, shash)
    filename = f"{a.source_date}--{slug}--{shash}.md"
    dest_dir = os.path.join(a.vault, a.subdir)
    os.makedirs(dest_dir, exist_ok=True)
    path = os.path.join(dest_dir, filename)

    # Idempotency: same source (hash) → same filename. If a complete map exists, skip.
    if os.path.exists(path) and len(open(path, encoding="utf-8").read().strip()) > 200:
        out("EXISTS", path, filename, msg="map already saved for this source; skipping")

    tags = [t.strip() for t in a.tags.split(",") if t.strip()]
    ordered_tags = ["mind-map"] + [t for t in tags if t != "mind-map"]
    related = [r.strip() for r in a.related.split(",") if r.strip()]
    related_yaml = "[" + ", ".join(f'"[[{r}]]"' for r in related) + "]"

    fm = {
        "title": a.title, "tags": "[" + ", ".join(ordered_tags) + "]", "type": "mind-map",
        "status": "active", "summary": a.summary.replace("\n", " ").strip(),
        "created": a.source_date, "updated": a.capture_date, "related": related_yaml, "aliases": "[]",
    }
    lines = ["---"]
    for k in HOUSE_ORDER:
        if k in ("tags", "related", "aliases"):
            lines.append(f"{k}: {fm[k]}")
        else:
            lines.append(f'{k}: "{str(fm[k]).replace(chr(34), "")}"')
    lines += [f'source: "{a.source.replace(chr(34), "")}"', f'source_hash: "{shash}"', "---", "",
              a.body.strip(), ""]
    content = "\n".join(lines)

    # Atomic write onto the mount + read-back verify.
    try:
        fd, tmp = tempfile.mkstemp(dir=dest_dir, suffix=".tmp")
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(content); f.flush(); os.fsync(f.fileno())
        os.replace(tmp, path)
    except Exception as e:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        out("ERROR", code=3, msg=f"write failed: {e}")
    if f'source_hash: "{shash}"' not in open(path, encoding="utf-8").read():
        out("ERROR", path, filename, code=3, msg="read-back verify failed")
    out("WROTE", path, filename)


if __name__ == "__main__":
    main()
