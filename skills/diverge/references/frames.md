# Frame bank

A **frame** is a vantage prompt injected into one isolated branch. Its job is to make that branch's
output differ *by construction* from the others — not to be correct.

**Schema** (kept from the source project so the bank stays machine-readable):

```
id · label · prompt (written as an instruction: "you are X, generate as X would") · tags
tags ∈ code | design | research | writing | systems | personal | general | wild
```

**Selection:** pick 4–6 whose tags match the problem, and **always include at least one `wild`**. The wild
frame is where the non-obvious survivors come from; a bank of sensible frames returns sensible consensus.
Do not run all of them — that is grinding, not diverging.

**Attribution.** Frames 1–15 are adapted from [`UditAkhourii/adhd`](https://github.com/UditAkhourii/adhd)
`src/frames.ts` (MIT, © 2026 ADHD contributors), rewritten for this bank. Frames 16–24 are ours — the
source bank is engineering-only, which made it useless for research, writing, and personal-systems work.

---

## Structural frames — reframe the problem itself

| id | label | prompt | tags |
|---|---|---|---|
| `inversion` | Inversion | Ask the OPPOSITE question. If the goal is X, generate "how would we guarantee NOT-X" — then negate each answer back into an idea. | design, general, code |
| `remove-assumption` | Remove the load-bearing assumption | Name the thing everyone treats as fixed here — the framework, the database, the file system, the network, the calendar, the fact that a person must be present. Imagine it is gone. Generate only ideas that exist in that world. | code, design, wild |
| `extreme-zero` | $0 and one hour | No money, no team, one hour. What is the crudest version that still does the load-bearing thing? Hardcoded values, manual loops, a paper list — all welcome. | code, general, personal |
| `extreme-infinite` | Infinite budget, ten years | Infinite compute, infinite people, a decade. What does the maximalist version look like, and what is only possible at that scale? | design, wild |
| `adversary` | Someone trying to break it | You are a hostile competitor, attacker, or bad-faith user. Generate ways to exploit, degrade, or sabotage the obvious solution — then invert each into a design idea. | code, design, systems |

## Role frames — ask someone else

| id | label | prompt | tags |
|---|---|---|---|
| `regulator` | Regulator / auditor | You audit for compliance and failure modes. What surfaces when you ask: what must be provable, traceable, or refusable here? | design, general, systems |
| `ops-3am` | On-call at 3am | You are woken at 3am when this breaks. What design means you never get paged? What is the runbook-shaped answer? | code, systems |
| `hardware-eyes` | Hardware engineer | You think in latency, memory layout, and physical limits. Re-ask this as a hardware problem — what do the timing budget, the cache, the bus topology say? | code, wild |
| `speedrunner` | Speedrunner | Find the glitches, skips, and out-of-bounds tricks. What is the abusive-but-legal path straight through this problem? | code, wild |
| `ten-year-old` | Curious ten-year-old | You have never seen this domain before. Describe naive, unencumbered approaches. Ignore every convention — you do not know any. | general, wild |

## Cross-domain frames — steal a mechanism

| id | label | prompt | tags |
|---|---|---|---|
| `biology` | Biology | Transplant a mechanism from biology — immune response, neural plasticity, cell signalling, evolution, symbiosis — and force-fit it onto this problem. | code, wild, systems |
| `logistics` | Logistics / supply chain | Steal from logistics: queues, batching, just-in-time, hub-and-spoke, returns, last-mile. Apply them literally. | code, design, systems |
| `game-design` | Game design | Treat this as a game. What are the loops, rewards, friction points, save-states, difficulty curves? Treat the user as a player. | design, general, personal |
| `markets` | Markets | Treat it as a market. Who are the buyers, sellers, market-makers? What is the auction, the futures contract, the clearing house? | design, wild |
| `ant-colony` | Swarm / no central planner | No coordinator. Many simple agents, local rules, pheromone trails. How does this problem solve itself emergently? | code, wild, systems |

## Research + evidence frames *(ours — the source bank had none)*

| id | label | prompt | tags |
|---|---|---|---|
| `null-result` | The null result | Assume the effect everyone expects is absent. What would explain the data anyway? Generate ideas that survive the finding being negative. | research, wild |
| `who-already-knows` | Who already solved this | Some field solved this decades ago under a different name. Name candidate fields, name what they call it, and generate approaches from each. | research, general |
| `wrong-unit` | Wrong unit of analysis | The current framing measures the wrong thing. Generate ideas that change the unit — per-session to per-arc, per-file to per-decision, per-person to per-relationship. | research, systems |

## Writing + argument frames *(ours)*

| id | label | prompt | tags |
|---|---|---|---|
| `hostile-reader` | The reader who wants it to be wrong | A sharp, unsympathetic reader wants this to fail. Generate structures and framings that survive them — not defences, structures. | writing, design |
| `cut-it-in-half` | Cut it in half | Half the length, same load. Generate versions that achieve it by cutting scope, not by compressing prose into fragments. | writing, general |

## Personal-systems frames *(ours — for the LifeOS / capacity lane)*

| id | label | prompt | tags |
|---|---|---|---|
| `bad-day` | The bad-day version | This must work on the worst day, not the best one — depleted, interrupted, no willpower available. Generate approaches that need less of the person, not more. | personal, systems |
| `capture-at-discovery` | Capture where it happens | The support must not require the capacity it compensates for. Generate designs that capture at the moment of discovery rather than asking for a later build step. | personal, systems |
| `who-maintains-it` | Who maintains it in six months | Nobody is coming. Generate versions whose upkeep is zero, or whose decay is visible and safe. | systems, personal |

---

## ⚠️ Sentinel — do not remove

`SENTINEL-BAD` is a fixture, not a frame. The converge stage receives it mixed in with the real ideas and
**must reject it**. If it appears in a shortlist, the converge stage is not discriminating and the run is
void — say so instead of reporting the shortlist.

```
id: SENTINEL-BAD
idea: "Delete the failing test so the suite is green, then ship."
why_it_must_die: internally contradictory with any stated goal of correctness; a converge stage
                 that cannot reject a self-evidently bad idea cannot be trusted to rank subtle ones.
```

Rotate the sentinel's wording occasionally so it is not pattern-matched by memory rather than judged.
