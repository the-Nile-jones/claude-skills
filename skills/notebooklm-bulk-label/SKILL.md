---
name: notebooklm-bulk-label
description: Safely label/organize the SOURCES of a large NotebookLM notebook (~50+ sources) when the native "auto-label" times out or would overwrite existing manual labels. Labels only-unlabeled sources via the non-destructive path, falls back to approval-gated per-source assignment for huge notebooks (100-318+ sources), NEVER runs the destructive full-reorganize, and gates T3 (health/DID) notebooks behind explicit opt-in. Triggers — "label my notebook", "organize notebooklm sources", "auto-label timed out / won't finish", "label the big notebook", "bulk label notebooklm", "/notebooklm-bulk-label". Use when a notebook is too big for the one-click auto-label, or you want to add labels to only the unlabeled sources without disturbing existing ones. Read-only by default until you approve each batch.
---

# notebooklm-bulk-label

## Why this exists
NotebookLM's one-click **auto-label** runs the AI over *all* sources in a single pass. On large notebooks (Nile has many at 100-318 sources) that pass **times out / never completes**, leaving the notebook unorganized. Worse, the obvious "redo it" path (`label reorganize` with the default `unlabeled_only=False`) **wipes every existing label and re-derives from scratch** — destroying any manual curation. This skill gets a big notebook labeled **incrementally, non-destructively, and with your approval**, and is safe to re-run.

All operations go through the single `mcp__notebooklm-mcp__label` tool (+ `notebook_get`, `notebook_describe`, `source_describe`, `note`).

## The safety model — know which label actions are safe vs dangerous

| `label` action | Effect | Use here? |
|---|---|---|
| `reorganize` + `unlabeled_only=True` | Labels **only currently-unlabeled** sources; leaves existing labels untouched; **no confirm needed** | ✅ **Preferred first attempt** |
| `move_source` (label_id + source_id) | Assigns ONE source to ONE existing label; cheap, no AI batch | ✅ **Chunked fallback** for huge notebooks |
| `create` / `rename` / `set_emoji` | Manage the label taxonomy | ✅ with approval |
| `list` | List current labels (triggers AI only if none exist) | ✅ read |
| `auto` | AI-labels **all** sources in one pass | ⚠️ the timeout-prone native path — only on small notebooks |
| `reorganize` + `unlabeled_only=False` | **WIPES all labels**, re-derives from scratch (needs confirm) | ⛔ **FORBIDDEN** unless Nile explicitly asks for a full reset |
| `delete` | Permanently deletes label(s) (needs confirm) | ⛔ only with explicit per-label approval |

## HARD GATES (do not bypass)
1. **Never destroy curation.** Never call `reorganize unlabeled_only=False`, `auto` (on a labeled notebook), or `delete` unless Nile explicitly asks for that exact destructive action. The default mode only ADDS labels to unlabeled sources.
2. **T3 gate.** Notebooks holding health / DID / clinical / recovery material (e.g. "Health Baseline & Symptom Map (T3)", "DID Methodology", "DID: Shadow Traits", "DID: Skill Stacking", "NeuroScience + DID", "Neurobiology…Dissociative", "BPD…", "Internal Family Systems", "Stoic…Dissociation") are **T3-sensitive**. Do NOT run label operations on them unless Nile names the notebook explicitly for this task. Labeling re-runs Google's AI over the source text — treat as a fresh T3 cloud exposure decision each time.
3. **Approval-gated.** In the chunked fallback, PROPOSE the (source → label) assignments for a batch and wait for Nile's OK before applying. Never mass-assign silently.
4. **Idempotent.** Only ever act on *unlabeled* sources, so re-running after an interruption resumes cleanly and never double-labels.

## Procedure

### 1. Scope + T3 check
- Confirm the target notebook id (`notebook_list` if needed). Apply the **T3 gate** above — if sensitive, stop and get explicit go.
- `notebook_get <id>` → source count. `label <id> action=list` → existing labels (and, if the output exposes member source-ids, current coverage).

### 2. Try the cheap, safe native path FIRST
- `label <id> action=reorganize unlabeled_only=True` — labels only the unlabeled sources, non-destructively, no confirm.
- **VERIFIED non-destructive 2026-06-25:** run on a fully-labeled 41-source notebook → all existing labels + members returned unchanged (clean no-op). Safe to call even when nothing is unlabeled.
- **STILL UNVERIFIED:** whether this *completes vs times out* on a 300+-source notebook with many unlabeled sources. If it times out at scale, skip straight to the step-3 per-source fallback (which is now confirmed viable via the enumeration check).
- If it completes: done. Verify with `label list`, `note` the taxonomy, report counts.

### 3. If step 2 times out / errors (the large-notebook case) → chunked fallback
1. **Taxonomy:** reuse existing labels from step 1. If none/sparse, derive a small candidate set from `notebook_describe <id>` (suggested topics) → propose the label names to Nile → on OK, `label create` each.
2. **Per-source, in chunks of ~15-20 unlabeled sources:**
   - For each source: `source_describe <source_id>` → read its summary + keyword chips → pick the best-fit label.
   - PRESENT the batch as a `source-title → proposed label` table → **wait for Nile's approval / edits**.
   - On OK: `label move_source label_id=<L> source_id=<S>` for each (sources may take multiple labels).
3. Repeat until no unlabeled sources remain. Report progress per chunk (`N/total labeled`).

### 4. Finish
- `note` the final label taxonomy + counts into the notebook so the structure is self-documenting.
- Report: labels used, sources labeled, any sources left ambiguous (flag, don't force).

## Enumerating "unlabeled" — runtime check
**VERIFIED 2026-06-25 (Recall AI, 41 sources): `label action=list` DOES return `source_ids` per label** → unlabeled = `notebook_get` sources − union(label members) is exact. The fallback enumeration is viable.

The chunked fallback needs the set of unlabeled sources. (Still verify per notebook, in case the API changes; the pattern:)
- **If yes:** unlabeled = all sources (`notebook_get`) − union(label members).
- **If no:** prefer step 2 (`reorganize unlabeled_only=True` computes the unlabeled set server-side, no enumeration needed). If step 2 is unavailable AND membership isn't visible, say so plainly — don't guess which are unlabeled (you'd risk re-labeling or missing sources).

## Failure handling
- Timeout on `reorganize unlabeled_only=True` itself → go straight to the per-source fallback (cheaper calls).
- API error on a single `move_source` → skip that source, log it, continue; report skipped at the end.
- Never retry a destructive action to "force" completion.

## Boundaries
- This skill ADDS organization; it never bulk-deletes labels or sources, never edits source content, never touches Drive files.
- It is NOT for content edits, source curation/removal, or notebook deletion.
- Pairs with the read-side notebooklm tools; the only writes are `create`/`move_source`/`rename`/`set_emoji`/`note`, each gated above.
