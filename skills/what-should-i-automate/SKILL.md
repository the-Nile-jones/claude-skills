---
name: what-should-i-automate
description: >-
  On-demand automation-gap audit — surfaces repetitive manual toil worth killing, weighted by LIVED pain-signal (frequency × friction from real recent work + conversation), not a static config scan. PULL-only: Nile invokes it when he has build-energy. Triggers — "/what-should-i-automate", "what should I automate", "what's worth automating", "what toil can I kill", "automation gaps". Anti-guilt by design (opportunities for when you have energy, NOT a backlog of shoulds), respects intentional-manual (flags Chesterton's-Fence cases, never asserts), and routes accepted candidates to skill-creator / Todoist / scheduled-tasks-manage rather than auto-building. NEVER schedule this skill — if asked to cron it, refuse and explain (a pushed "here's more you haven't done" report is a guilt-generator). Complements the always-on skill-candidate-diagonal + Shadow-Offload rules; this is the deliberate deep pass. On-demand only — never auto-fire.
---

# what-should-i-automate — On-Demand Toil Audit (PULL-only)

A deliberate hunt for repetitive manual work worth automating — run **only when Nile asks**, because he has the build-energy in that moment. This skill exists in hypothesis-tier (10×10× c_r≈0.42, 2026-06-15): the *idea* is sound, but it survives **only** as a pull-tool with the four guardrails below. Violate any one and it becomes net-negative.

## The four hard constraints (these ARE the skill — from the 10×10× kills)
1. **PULL, never PUSH.** Never scheduled, never a cron, never volunteered. If Nile (or any config) asks to schedule/cron/automate the running of this skill → **refuse and explain**: a monthly "here's more you haven't done" report is a shoulds/guilt generator for a burnt-out, backlog-heavy, no-new-habits regime. The whole point is he runs it when *he* wants to build.
2. **Pain-signal first, config-scan last.** The best gap-signal is lived friction — which task annoyed him, how often he did it by hand — visible only in real work, not a static file scan. Weight conversational/session/Todoist friction above infra-config toil.
3. **Anti-guilt framing.** Output = a SHORT menu of *opportunities*, framed as "when you have energy, this kills X pain" — never "you should have automated this." Honor [[feedback_dont_underestimate_capacity]] + [[feedback_shame_guilt_fear_watch]]. If burnt-out/low-Mana signals are present, return fewer candidates, lighter touch — or just the single highest-pain one.
4. **Respect intentional-manual (Chesterton's Fence).** Some things are manual *on purpose* (e.g. YNAB new-txn approval = Nile's deliberate control point; irreversible/financial/judgment ops). For any candidate that might be deliberate, **flag it as "keep-manual?" and ask** — never assert "automate this." Cross-ref [[feedback_always_ask_list]] + Chesterton's Fence.

## Signal sources (pain-weighted, high → low)
1. **Lived friction (highest weight)** — repetitive manual steps in *this* session + recent conversation: what did Nile do by hand more than once? what did he sigh at? Pull from session context + the capture buffer (`_PARA/_Inbox/claude-session-capture.md`).
2. **Recurring task patterns** — Todoist tasks he keeps re-creating, or that recur manually (the Shadow-Offload "3+ times" signal). `mcp__todoist__*` recent/recurring.
3. **Workflow/infra toil (lowest)** — manual multi-step sequences in scripts/ops that a wrapper would collapse. Lightweight; the `config-drift-scan` surface. Don't lead with this — it's the static-scan trap.

## Scoring & output
Per candidate: **frequency × friction × automatability − intentional-manual penalty.** Rank, then return Nile's recommendation format:
- **Top 3–5 (cap small — anti-overwhelm), ranked.** For each: the toil it kills · how often it bites (the pain) · **Spoon Cost (1–5)** to automate · **First Brick** (smallest start) · a **"keep-manual?"** flag where Chesterton applies.
- If nothing clears the bar, say so plainly ("nothing worth the spoons right now") — a clean empty result is a valid, honest answer, not a failure to find work.

## Routing accepted candidates (surface → Nile picks; never auto-build)
- **Repeatable procedure** (workflow with steps) → `skill-creator` (the skill-candidate-diagonal).
- **One-off action** → Todoist task (action-verb-first).
- **Genuinely periodic + low-guilt** (e.g. a backup check) → `scheduled-tasks-manage` (notify-on-fail wrapper). Apply the cron-vs-pull judgment honestly — most "automations" are better as pull-tools too.

## Boundary
The always-on `skill-candidate-diagonal` + `Shadow Offload` rules already surface gaps passively *during* work (this is correct and should keep happening). This skill is the **deliberate, on-demand deep pass** for when Nile sets aside energy to hunt toil — it does not replace the passive rules, and it must add the pain-weighted ranking they don't.
