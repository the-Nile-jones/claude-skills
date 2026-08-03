---
name: zero-as-answer
description: >-
  Read-only audit that hunts the silent-failure family — code where an ABSENCE is quietly treated as
  a RESULT, so "I looked and found nothing" and "I couldn't look" produce the same output and the
  second one hides inside the first. Finds guards that skip a missing file without warning, parsers
  keyed on a marker whose absence yields 0 instead of an error, HTTP calls that exit 0 on a 401,
  swallowed exceptions, and success paths that never assert what they actually produced. Scans →
  reports → hands fixes to /change-discipline; NEVER auto-fixes. Use this WHENEVER Nile says "silent
  failure", "why didn't this fire", "this said it worked but nothing happened", "audit my scripts",
  "is this actually running", "the log looks healthy but", "check for silent failures", "zero as
  answer", "/zero-as-answer" — and proactively any time a script, cron, hook, or backup reports
  success while a downstream artifact is missing, empty, stale, or zero. Also use when reviewing NEW
  code that counts, parses, fetches, or backs up anything: the cheapest time to kill this bug is
  before it ships. SKIP for ordinary bug-hunting with a known reproducer (that's /systematic-debugging),
  for config references pointing at dead paths (that's /config-drift-scan — complementary, not this),
  and for general code review (/adversarial-reviewer).
---

# zero-as-answer

## The disease

Look at these five real failures. They are the same failure.

| What happened | What the code said | What was true |
|---|---|---|
| `dump_sqlite` hit a deleted database | *(nothing — skipped)* | The backup silently covered less than we thought, for 7 weeks |
| `awk` counted entries under a heading that didn't exist | `0 pending` | 153 entries were pending |
| A retainer scanned for a `## Merged log` heading that didn't exist | *(retained nothing)* | It had never retained anything, ever |
| `curl` got an HTTP 401 | `exit 0` | Auth was broken |
| A `grep` filter didn't match a line | *(line absent from output)* | The line was there; the filter was wrong |

The shallow name for this is "silent failure." That name is a trap, because it sends you hunting for
missing error messages — and error messages are the symptom, not the disease.

**The disease is that zero is overloaded.** Every one of those cases conflates:

- **an authentic zero** — I measured, and the answer is genuinely none — with
- **an unmeasurable zero** — I could not measure, so I have no answer.

They produce identical output. And because a healthy system produces plenty of authentic zeros, the
unmeasurable ones hide in plain sight wearing the same clothes. That is why these bugs survive for
weeks with a green log: *nothing is broken, in the sense that nothing reports being broken.*

Once you see it this way the fix stops being "add a warning" and becomes something sharper:
**every query that can return zero must be able to say which zero it is.**

## What this skill does

Three moves, in order. The first is mechanical, the second is easy, the third is the one that matters.

### 1. Find where an absence is being treated as a result

Signature patterns worth grepping for. **None of these is a bug by itself** — see the precision
section below, which is the load-bearing part of this skill.

**Guard-skip** — the check that quietly does nothing:
```bash
if [[ -f "$src" ]]; then ...; fi        # no else. Missing source = silence.
[ -d "$dir" ] && do_thing               # same shape
```

**Marker-keyed parse** — a count or extraction keyed on a literal that might not exist:
```bash
awk '/^## Heading/{f=1} f && /^- /{c++} END{print c+0}'   # no heading -> prints 0, not an error
grep -c 'marker'                                           # absent marker -> 0
```
```python
text.split("## Heading", 1)[1]      # absent -> IndexError (loud, fine)
d.get("key", 0)                     # absent -> 0 (silent, dangerous)
```

**Unbounded section parse** — reads past the section it claims to read:
```python
body = text.split("## Merged log", 1)[1]   # takes EVERYTHING after. No stop at the next "##".
```

**Unchecked network** — a failed call that looks like an empty one:
```bash
curl -s "$url"                      # no --fail, no %{http_code}: a 401 body is just "data"
```

**Swallowed error** — the explicit ones:
```python
except Exception: pass
```
```bash
cmd 2>/dev/null || true             # on a load-bearing call
```

**Success-by-absence-of-error** — the subtlest and most common:
```bash
tar -cf "$out" "$src" && log "[OK] backed up"   # OK = tar didn't crash. Not: the archive has contents.
```

### 2. Make the absence loud

The cheap half. An absent input that the code *depends on* should log, warn, or exit — not shrug:

```bash
if [[ ! -f "$src" ]]; then
  log "[MISSING] expected source absent, nothing dumped: $src"
  return 1
fi
```

### 3. Assert the positive — this is the one that actually prevents recurrence

Making absence loud fixes the instance. Asserting the positive fixes the *class*.

Checking for the absence of errors is not the same as checking for the presence of the result.
A backup that reports `[OK]` because `tar` didn't crash tells you nothing about whether it archived
anything. The question to ask of every success path is: **what did you expect, and did you get it?**

```bash
# Weak: no error occurred.
dump_sqlite "$a"; dump_sqlite "$b"; dump_sqlite "$c"; log "[OK] backups done"

# Strong: declare the expectation, then assert it.
EXPECTED=3; DUMPED=0
dump_sqlite "$a" && ((DUMPED++)); dump_sqlite "$b" && ((DUMPED++)); dump_sqlite "$c" && ((DUMPED++))
(( DUMPED == EXPECTED )) || log "[MISMATCH] expected $EXPECTED dumps, got $DUMPED"
```

The mismatch line is what would have caught the ChromaDB bug on day one instead of week seven.
Wherever you find an absence-as-result, ask what the *expected* count, status, or byte size was —
and whether anything anywhere checks it.

## Precision is the whole game

**Most guards are fine.** `if [[ -d "$HOME/.openclaw" ]]` around an optional component is correct
code, not a bug. A skill that flags every `-f` test will flag hundreds of lines, get ignored within a
week, and leave the real bugs exactly where they were. That failure mode has already happened here:
a keyword scan of the capture buffer flagged 36% of entries and was thrown away for it.

So the judgment that separates a finding from noise is a single question:

> **Is this thing load-bearing — is the script's stated job undone if it's absent?**

- `dump_sqlite` on a database the backup **claims to protect** → load-bearing. A finding.
- A guard around an **optional** feature that may legitimately not exist → correct. Not a finding.
- `2>/dev/null` on a **best-effort** cleanup → fine.
- `2>/dev/null` on the **fetch whose output the script then reports as truth** → a finding.

You cannot answer that from the pattern alone. You have to read what the script says it does — its
header comment, its log lines, its name — and ask whether this absence would make it a liar.

**When unsure, drop it.** A missed finding costs one bug. Ten false findings cost the skill.

## Output

Report only. Never edit. Never fix. Fixes are handed to `/change-discipline`, which is where changes
to 3+ files belong — and an audit of this kind routinely produces more.

```markdown
# zero-as-answer — <scope> — <date>
**Scanned:** <n> files · **Findings:** <n> · **Dropped as benign:** <n>

## Findings — ranked by blast radius
### 1. <file>:<line> — <one-line statement of the lie the code tells>
**Pattern:** <guard-skip | marker-keyed parse | unbounded section | unchecked network | swallowed error | success-by-absence>
**Load-bearing because:** <what the script claims to do, and why this absence makes that claim false>
**Silent since:** <when, if determinable — "7 weeks" lands differently than "recently">
**Blast radius:** <what has been quietly not happening>
**Fix shape:** <make-absence-loud | assert-the-positive | both>

## Dropped as benign (<n>)
<bare list — pattern matched, but the absence is legitimate. Shown so the reader can check my judgment.>

## Recommended next step
<usually: /change-discipline over the N files above>
```

Say what you dropped and why. A reader must be able to audit the auditor — otherwise this skill is
just one more thing that reports success while measuring nothing.

## It is not only code

The same bug lives in reasoning, and it is worth naming because it is harder to see there.

During the session that produced this skill, Claude hit it three times in one night:
- Filtered `curl` output through a `grep` whose pattern happened not to match one attribute, then
  reported the attribute as **missing** — and called it a bug. The absence was in the filter.
- Printed a hardcoded verdict (`VOID`) that its own computed output contradicted two lines above.
- Asserted a tool didn't exist that had been built the day before.

Every one is the same move: **treating absence of evidence as evidence of absence, at speed.** When
this skill is running and something turns up empty — a grep with no hits, a query with no rows, a
directory with no files — the discipline is identical to the one it audits for: *did I look and find
nothing, or did I fail to look?* Verify the instrument before believing the reading.

## Neighbours (don't duplicate them)

- **`/config-drift-scan`** — checks whether configs *point at* things that still exist. This checks
  whether code *notices* when they don't. Complementary; run both, they find different bugs.
- **`/backup-integrity-check`** — verifies specific backups landed. This finds the *class* of code
  that would let a backup vanish unnoticed.
- **`/systematic-debugging`** — for a known bug with a reproducer. Use that instead when you already
  know something is broken. This skill is for what you *don't* know is broken.

---

## Two new members of the family (added 2026-07-13 — both from real near-misses)

**7. The query against a field that doesn't exist.**
`WHERE a.text CONTAINS $x` on nodes whose property is actually `.statement` → every comparison is null → **`NOT FOUND` for everything.** A search that *cannot* succeed always finds nothing, and that is byte-identical to "it isn't there." **Nearly deleted 60 atoms whose only other copy I had just declared missing.**
⇒ **Before trusting a negative, prove the query finds a KNOWN-PRESENT item.** Dump `keys(sample)`. Never assume a field name.

**8. The instrument that hasn't finished.**
A `grep` over a slow network mount was **still running** when I reported "not found anywhere." It later returned a hit. **"Still looking" is not "looked and found nothing."**
⇒ **No conclusion from an unfinished check.** If it hasn't returned, you have no answer — say *"still running."*
⇒ **Corollary: grep the DOCS before the DATA.** The checklist file had the complete answer already written down. **Four times in one day the falsifier was already on disk and I re-derived past it.**
