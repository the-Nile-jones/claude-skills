---
name: atom-cypher-safe
description: >-
  Safe write-layer for the Exocortex Master Atoms Library (Neo4j SSoT, ~569 Atom nodes, writable via mcp__neo4j-cypher__*). Gates destructive Cypher (a stray DETACH DELETE / bad MERGE wipes or corrupts the whole atom SSoT — only the weekly CSV export recovers it), enforces atom schema conformance, runs dedup before insert, writes the validation_log.jsonl registry line, and read-back-verifies every write. Use whenever adding, refining, deleting, or bulk-writing atoms via Cypher, or running any mutating mcp__neo4j-cypher__write query. Triggers — "add an atom", "port atoms", "refine atom", "write to Neo4j", "Cypher write", "DETACH DELETE", "atom candidate", "/atom-cypher-safe". Pairs with pattern-extraction (which PRODUCES atoms → hands off here for the safe write) and infra-safe (which gates Docker/volume ops; Neo4j atom Cypher routes HERE). SKIP for read-only Cypher (MATCH/RETURN, get_neo4j_schema) — run those freely. On-demand: suggest it, don't auto-fire.
---

# atom-cypher-safe — Safe Atom Writes to the Neo4j SSoT

The atom library is the Exocortex SSoT and it is **writable via raw Cypher with no gate** — one bad mutation corrupts or wipes ~569 atoms, recoverable only from the weekly CSV export + a Neo4j regen. This skill is the discipline layer between "I have an atom to write" and the live store. The MCP gives the *capability*; this adds *schema conformance, dedup, destructive-op gating, and read-back*.

**Schema SSoT = `memory/reference_atoms_library.md`** — read it, don't hardcode the schema here (it drifts; the old 17-col Sheet schema is dead — Neo4j is simpler). As verified there:

- **Atom props:** `atom_id, statement, family, tags, source, status, load_bearing, did_specific, confirmation_count`.
- **`confirmation_count`** (added to this doc 2026-07-09; promoted to the canonical write schema by pattern-extraction v3.1 on 2026-06-22) — honest integer, the number of **distinct-provenance** sources that independently assert the atom. **Starts at 1** on creation. Increments ONLY on distinct-provenance re-confirmation — never a same-source re-run, never a mutually-citing echo. It drives the Provisional (1) / Tested (≥2 incl. a Tier-1/2 source) tier. It is the one number that is *counted*, never eyeballed. **Set it on every CREATE.** Its absence on ~543 older atoms is migration backlog, not permission to omit it.
- `status` = `Active` | `Candidate` — **new atoms enter as `Candidate`**.
- `load_bearing` / `did_specific` = `"Yes"` | `"No"` (string).
- `tags` = comma-separated string. Cross-refs go in `tags` (no `RELATED` edge).
- Only inter-atom edge = `TESTED_BY` (DMA layer: `Song→[:PRODUCED]→DMA_Result←[:TESTED_BY]←Atom`).
- Connection: GSM `NEO4J_PASSWORD` (call inline, never echo).

## Classification
- **GREEN (run freely):** `MATCH … RETURN`, `get_neo4j_schema`, COUNT, any read.
- **YELLOW (proceed + read-back):** single-atom `CREATE`/`MERGE` of a new Candidate; a scoped `SET` refining one atom by `atom_id`.
- **RED (stop + confirm + snapshot first):** any `DELETE`/`DETACH DELETE`; `MATCH` without a tight `WHERE`/`atom_id` bound feeding a write; bulk `SET`/`MERGE` over many nodes; anything that could touch >1 atom unintentionally.

## Safe-write flow
1. **PREFLIGHT** — snapshot the blast radius: `MATCH (a:Atom) RETURN count(a)` (baseline; ~569 as of 2026-07-09 -- read it live, never hardcode; the count grows) + return the exact target rows you intend to change. A write whose match set is larger than intended = STOP.
2. **DEDUP (adds)** — before `CREATE`, search for an existing atom covering the same claim: venn-scan (`~/Exocortex/venn-scans/`) or `MATCH (a:Atom) WHERE a.statement CONTAINS … / a.family = …`. If a near-dup exists, refine it (`SET`) rather than create a twin.
3. **CONFORM** — assemble props to schema: assign next `atom_id` in the family (e.g. `A-PKM-15`), `status:'Candidate'`, `load_bearing`/`did_specific` as `"Yes"`/`"No"`, **`confirmation_count: 1`**, `source` = the MA session / origin, `tags` comma-string with cross-refs. ⚠ Do NOT copy a sibling atom's prop set blindly to infer the schema — most live atoms predate `confirmation_count` and omitting it is how the migration stalls (this is exactly how a live atom got created without it).
4. **CONFIRM (RED only)** — for any delete/bulk op: state exactly which atoms and the rollback (CSV export path + regen); explicit nod before running.
5. **EXECUTE** — `write_neo4j_cypher`; deletes get a `WHERE a.atom_id = …` bound, never an open match.
6. **REGISTER** — append the dedup-registry line to `validation_log.jsonl` (existing convention — see PKM/MEM family precedent).
7. **VERIFY** — read-back: `MATCH (a:Atom {atom_id:'…'}) RETURN a` confirms the write; re-run the COUNT and confirm the delta is exactly what you intended (e.g. 569→570 for one add, not 569→0; a REFINE must show delta 0).

## Recovery (if a destructive write lands wrong)
SSoT regen source = the auto-refreshed CSV `_PARA/Resources/master_atoms_library/MA-FULL-LIBRARY-atoms-CURRENT.csv` (weekly `atom-export-refresh.timer`, ≥400-row sanity gate) + dated snapshots. Re-derive via `~/.local/share/atom-export/` tooling. A destructive op BEFORE the next weekly export means up-to-a-week of new atoms are only in your session record — snapshot manually before any RED op.

## Boundaries / cross-refs
- **pattern-extraction** ends at "Port + Anchor" — it produces atoms; route the actual write through this skill.
- **infra-safe** gates Docker/volumes (Neo4j runs in Docker — `volume rm` = total loss); row-level atom Cypher is gated HERE.
- Atoms are deliberately **NOT** mirrored to Hindsight (pruned 2026-06-09) — do not retain atoms to the memory layer.
