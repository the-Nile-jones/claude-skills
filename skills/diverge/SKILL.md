---
name: diverge
description: >-
  Generate a genuinely WIDE set of options for one open question by fanning out independent,
  context-isolated agents under different named cognitive frames, then converging to a short list plus
  the traps. Use this when the first three answers all sound like the same answer, when a naming /
  architecture / positioning / approach decision feels prematurely settled, or when Nile says "what
  else", "give me options", "widen this", "what am I not seeing", "diverge", or "/diverge". The point is
  BREADTH BEFORE COMMITMENT — it exists because a single context anchors on its own first idea and then
  defends it. SKIP when: the answer is a lookup, the root cause is already known, the question is closed
  ("quick", "standard", "canonical", "textbook", "just tell me"), a decision is already made and this
  would re-litigate it, or the task is execution rather than choice. It is deliberately expensive —
  roughly one agent per frame plus a converge pass — so it asks before spending.
---

# diverge

> **Inherits** `~/.claude/rules/nile_patterns.md` § *Skills Inherit These* — ceremony ∝ stakes (this skill's full pipeline is its maximum, not its floor) · one recommendation, not a manufactured slate · the procedure is not the deliverable · signal codes outrank this skill's verbosity · **dedup before proposing anything new**.

## Why this exists, and what it is NOT

A single context is a bad idea-generator for one specific reason: it commits early and then argues for the
commitment. Three "alternatives" produced in one thread are three samples from the same neighbourhood.

**This skill is already half-owned by three installed skills. Read this before assuming it is new.**

| Existing | What it does | How `diverge` differs |
|---|---|---|
| `adversarial-reviewer` | 3 named personas (Saboteur / New Hire / Security Auditor) find issues | Those personas run **in one context** and **critique existing work**. This generates, and the branches genuinely cannot see each other. |
| `article-review` | 8-lens bank + the `NxN` dial | Same — critique of a written artifact, one context. |
| `interview-mode` | "Open the aperture first… the first plausible frame is a *trap*" | That is the **diagnosis** this skill acts on. ⛔ Tier C, consent-gated — cite it, never auto-fire it, never absorb it. |

⇒ The only two things `diverge` adds: **genuine context independence** and **generation rather than
critique**. If a run does not need both, one of the three above is the cheaper right answer — say so.

**Relationship to `brainstorming`:** `brainstorming` claims *"before any creative work"* and forbids
invoking other skills. It is a **one-question-at-a-time requirements interview** that narrows toward a
spec. `diverge` runs **upstream** of it — widen first, then hand a shortlist into its interview. Never run
`diverge` inside a `brainstorming` session; finish or exit that first.

## Phase 0 — Pre-flight (always; it is three questions and it is allowed to abort)

**1. Is the question actually open?** Abort and answer directly if it is a lookup, a known root cause, or
phrased closed (*"quick"*, *"standard"*, *"canonical"*, *"textbook"*, *"just tell me"*). If Nile typed
`/diverge` explicitly, **skip this check — he opted in, do not second-guess him.**

**2. Say what it will cost, then ask.**

> This is ~N agent calls (one per frame) plus a converge pass, and maybe 30–90s. Worth it here?

Do not silently spend it. The source project's own docs disagree with themselves by ~4× on cost
(README "1.9× output tokens" vs skill body "5–10×") because the real expense is context reload per
branch, not output. Assume the larger number.

**3. Pick 4–6 frames from `references/frames.md`,** matching tags to the problem, **including at least one
`wild`**. Name them out loud. Fewer good frames beats grinding the whole bank.

## Phase 1 — Diverge (isolated, mechanically restricted)

Spawn **one agent per frame, in a single message so they run concurrently**, each with `subagent_type:
read-only-scout`.

🔴 **`read-only-scout` is not a suggestion — it is the enforcement.** Its `tools: Read, Grep, Glob`
frontmatter is an exclusive allowlist, so a branch is *mechanically incapable* of writing. Do **not** use
`general-purpose` with a "don't write anything" instruction: that is `X-AGT-01` (prompt-as-enforcement),
the exact anti-pattern behind the 2026-06-17 incident, and it is how the source project ships.

Each branch gets **only**: the problem, any context Nile supplied, its own frame prompt, and this
instruction. It does **not** get the other frames, or any other branch's output.

> You are generating, not judging. Produce 6 short, distinct ideas under this frame — one sentence
> each, plus one clause of rationale. Do not rank, evaluate, hedge, or caveat.
> The first three obvious answers are banned; those are the ones everyone already has.
> You may read the repo or corpus for grounding, but you cannot write anything.
> Return a JSON array only: `[{"idea": "...", "why": "..."}]`

⛔ **The isolation invariant.** Branches must be parallel and blind to each other. Do not serialise them,
do not feed one branch's output to another, do not "summarise the others first." Branches that see each
other anchor each other and the whole method collapses into one wider thought — at N× the price.
Independence buys non-overlap; the *frames* buy coverage (`A-AGT-05`). You need both.

## Phase 2 — Converge

Collect every branch's ideas into one list. **Inject the `SENTINEL-BAD` fixture from
`references/frames.md`** into that list, unlabelled, before judging.

Then, in the main context:

1. **Cluster** near-duplicates across frames. An idea that three frames reached independently is a
   different kind of signal from one only the `wild` frame found — note which, but do not treat
   convergence as correctness.
2. **Shortlist 3–5.** Include at least one non-obvious survivor, or say plainly that there wasn't one.
3. **Name the traps** — the ideas that look good and are not, with the reason each dies.
4. **Take a position.** *"Here are 20 ideas, you decide"* is the cop-out this skill exists to avoid.

### 🔴 No scores. Veto, not vote.

Do **not** rank ideas 1–10, do not emit a rubric, do not print a decimal. `pattern-extraction` v3 was
rewritten specifically to remove that layer: *"No decimal unless a tool actually computed it"* and
*"**Veto, not vote** — one well-grounded counterexample rejects the item regardless of how many other
tests passed."* Apply that here.

Two independent reasons, both load-bearing:
- **`X-ARS-01`** — scoring against a self-made rubric optimises the rubric (Goodhart). The source
  project's evals show exactly this: its huge deltas sit on dimensions its own output format
  guarantees, while its one format-neutral dimension moved **+0.83** at n=6.
- **`X-AGT-06`** — voting ensembles collude. Use one converge pass with a stated reason, not a panel.

### ⚠️ The sentinel gate

If `SENTINEL-BAD` survives into the shortlist, **the converge stage is not discriminating. Report that
and void the run** — do not present the shortlist as if it were trustworthy. A check never shown capable
of failing cannot distinguish "clean" from "broken."

## Phase 3 — Report

Lead with the answer, not the machinery (*the procedure is not the deliverable*).

**Mandatory accounting line — absence and failure must be distinguishable:**

```
Frames run: 5 of 5 returned · 0 empty · 0 malformed
```

A branch that returned nothing, timed out, or emitted unparseable output is **named**, never silently
absorbed. Malformed output is expected in practice, not exceptional. If fewer than half the branches
returned, say the run was thin rather than presenting a confident shortlist.

Then: the shortlist with a taken position · the traps · one line on what the wild frame contributed
(or that it contributed nothing).

## Baseline mode — `--baseline`

Runs the same problem **once, in one context, with all frames listed in a single prompt**. No fan-out.

This exists because the claim "independence beats one-context-multi-frame" is **untested by anyone**,
including the project the frames came from — its evals compared against a *single-shot* baseline, which is
a strawman for that claim. Run `--baseline` occasionally on a real question and compare. If the isolated
version stops earning its cost, that is a finding worth having, and this skill should shrink to a prompt
template.

## When this skill is the wrong tool

- The decision is already made → re-litigating it is a rabbit hole with good manners
- One good frame would do → just ask that one question directly, in-context
- The work is execution → `diverge` produces options, not progress
- It is tender / T3 / personal material → ⛔ `sounding-board` and `interview-mode` own that ground, and
  they are consent-gated. Do not fan out agents over Nile's life.
- Nile said *"I have work to do"* → stop generating options; give the First Brick

## Self-test

1. Run on any real open question. Confirm the report includes the `N of M` line.
2. Confirm `SENTINEL-BAD` was rejected.
3. **Control (both directions):** remove the sentinel-rejection step and re-run — the run must now report
   a broken converge stage. If it still reports a clean shortlist, the gate is decorative.
4. Confirm branches were dispatched as `read-only-scout`, not `general-purpose`.

## Provenance

Frames adapted from [`UditAkhourii/adhd`](https://github.com/UditAkhourii/adhd) (MIT) — the mechanism was
worth taking, the packaging was not. Full evaluation, including why that project's evidence does not
support its headline numbers and why `caveman` was rejected outright: KB *Divergent Ideation — Three
Repos, What Survived Review (2026-08-02)*.

Atoms: `A-AGT-05` (independence ≠ diversity; frames are the coverage mechanism — refines `A-AGT-02`) ·
`A-AGT-03` (a subagent's value is the clean slate) · `X-AGT-01` (prompt-as-enforcement) ·
`X-AGT-06` (voting ensembles collude) · `X-ARS-01` (Goodhart on a weak proxy) ·
`A-ARS-01` (define the convergence criterion before iterating).
