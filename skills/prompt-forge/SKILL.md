---
name: prompt-forge
disable-model-invocation: true
description: >-
  Shape a rough task into a strong, paste-ready PROMPT — the deliverable is the prompt itself,
  not the task's result. Most valuable when the prompt is going ELSEWHERE (a fresh session, a
  subagent brief, another machine, a teammate) or when Nile explicitly wants to see/refine the
  framing before committing. Triggers: /prompt-forge, "help me write a prompt", "frame this ask",
  "how should I ask you/Claude to X", "what's a good prompt for X". SKIP when he wants the task
  DONE now by THIS session (just do it — ask only if you hit a real gap), when he's
  exploring/diagnosing a problem (interview-mode), designing a feature before building
  (brainstorming), co-authoring a document (doc-coauthoring), or versioning production prompts
  (prompt-governance).
---

# prompt-forge

Help Nile turn a rough intent into a prompt that gets a great result on the first or second try.
You are the drafter: he gives the gist, you do the shaping. He should never have to compose the
full prompt himself — that's the point.

## First: does this skill even apply? (decline fast if not)

The skill has to beat "just tell me the task." Often it doesn't, so check before drafting:

- **Is the prompt going somewhere other than this conversation?** A fresh Claude session, a
  subagent brief, another machine, a teammate, a paste into claude.ai. **This is the sweet spot** —
  the target Claude won't have this context, so a well-framed prompt genuinely pays off.
- **Or does Nile explicitly want to see/refine the framing** before he commits to running it?
- **Otherwise — he wants THIS session to do the work now.** Then forging is a describe-it-twice
  ceremony. Decline: *"just tell me — I'll ask if I hit a real gap,"* and do the task. Making him
  restate a task as a prompt to the same agent is exactly the over-composition friction he fights.

If the rough task **already** has a clear goal, named scope, and an obvious check, don't re-shape it
to prove the skill ran — say *"that's already a strong prompt, paste it as-is"* and stop.

## The flow

1. **Take the rough task** — one line is fine.
2. **Draft the prompt**, applying the defaults below for anything unspecified. Keep it short (see
   the stakes gate). Emit the prompt **first, always** — never withhold it behind a question.
3. **Make your assumptions visible** in an `assumed:` line (he can't see your reasoning; this is how
   he vetoes a wrong default in one word).
4. **Questions are rare.** Defaults win — most forgings ask zero. The one honest exception: if the
   task is so thin you'd be guessing **3+ load-bearing levers** (goal, scope, target all unknown),
   don't bury five guesses in one `assumed:` line — either ask **one** framing question, or draft
   **two divergent interpretations** and let him point. That's not over-asking; that's an absent
   target. Put any such question on an `open:` line *below* the prompt, so the draft stays usable.
5. **Refine at most once**, then push to act: *"good enough — want me to just run this now?"*
   Polishing a prompt about a task, forever, is motion not output — cap it.

## Match the stakes (this governs how much prompt to write)

Ceremony scales with the task, or the skill becomes the bloat it's meant to prevent.

- **Trivial / reversible / single-file** (fix a typo, rename a var, one-line tweak): **Goal +
  Output only. 2–4 lines. No `assumed:` line needed.** Do not invent a verification step or a
  plan-gate for something a glance would undo.
- **Load-bearing** — and only when you can *positively identify* it as multi-file, touches
  config/prod, or destructive (not merely "reversibility unknown"): add the plan-gate, a real
  verification loop, and explicit scope.
- **Prompt length budget: ~4–12 lines; hard ceiling ~20.** If it's longer, you're micromanaging
  tool sequences the model already knows (git, commits, file search) — cut them.

## The levers

Thread in the ones that matter for *this* task; let the model's native competence cover the rest.
Boris Cherny (created Claude Code) notes you don't have to tell it which tools to use — it strings
them together itself; over-specifying is wasted lines.

1. **Goal + success criteria.** What "done" looks like, concretely. When the task has a checkable
   output, write success as the thing to check — then it doubles as the verification target (lever 4).

2. **Plan-first vs one-shot** *(only this — approval/gating lives in lever 5)*. For load-bearing work,
   say *brainstorm → make a plan → run it by me → wait before executing*. Boris: *"the easiest way to
   get the result you want is ask it to think first."* Also Nile's Plan-Mode default. Trivial → skip.

3. **Context to hand over.** Name the specific files / prior decisions / the relevant CLAUDE.md —
   don't say "look around." Boris's general point is *more relevant context = better decisions*; the
   "keep it short" caveat is specifically about an over-long CLAUDE.md eating the window, not a reason
   to starve the prompt. So: give what's needed, scoped, not dumped.

4. **Verification loop — the highest-leverage lever, *where a truth condition exists*.** Boris ranks a
   self-check feedback loop as *"probably the most important thing… it will 2-3x the quality"* — but
   he means a loop the model runs against its **own output and iterates on**: the failing test, the
   diff, the screenshot, a control grep. That is different from just speccing the task carefully.
   Give it one when the task has a real pass/fail. When the output is genuinely subjective (a draft,
   a judgment call, brainstormed options), **say so honestly** — *"no automated check; success is
   Nile's read"* — never bolt on a fake check (a word-count on grief writing is theater, and it
   violates his run-the-control rule: a real control returns differently when the instrument breaks).

5. **Scope + guardrails.** What's in, what's explicitly **ruled out**, what NOT to touch, and any
   approval / reversibility / destructive gate (all gating lives here). For 3+-file or destructive
   work, name the discipline: back up first / `/change-discipline` / "show me the diff before applying."

6. **Output shape.** Format, length, destination. Terse by default (his standing pref) unless he
   wants depth. Where relevant, **show one small example** of the output shape you want — a sample
   line, the table header, the JSON key — it's cheap and pins the format better than describing it.

**Domain note — these re-map for non-code work.** For prose / research / corpus / personal tasks:
verification becomes *read-back against the source / cite the passage / does it match his voice*;
context becomes source docs not code files; the plan-gate usually drops. Don't force the code register
onto writing or research.

## Output format

```
Here's a prompt for it:

---
<the forged prompt, ready to paste>
---

assumed: <≤3 comma-separated clauses, one per NON-obvious default; skip any that's self-evident
from the prompt; omit this line entirely on trivial tasks>
open (only if needed): <≤1 framing question, or "interpretation A vs B?">
```

Write the forged prompt in Nile's register — direct, concrete, no filler, as if briefing an engineer
(or for prose, a sharp collaborator). Natural language, not a rigid template.

## Examples

**Code — real verification loop.**
Rough: *"the health-sync script keeps dropping records, fix it"*
```
The nightly health-sync (~/scripts/health-sync.py) is dropping records — find and fix the cause.

First reproduce: run it against the test fixture and show me which records go missing vs the
input. That count IS your feedback loop — the fix isn't done until it's zero and the existing
tests still pass. If the fix spreads beyond the sync function, show me the plan before editing.

Success = re-run on the fixture drops zero records, suite stays green.
```
`assumed: reproduce-first with the fixture as the check; plan-gate only if it spreads past one function.`

**Non-code — verification re-maps to read-back, no fake check.**
Rough: *"help me prompt claude to summarize the polyvagal KB note for the dissertation"*
```
Summarize "KB/KB/Polyvagal Theory (2026-05-26).md" for the dissertation lit-review — ~200 words,
my academic register. Pull ONLY from that note; don't add outside claims. Cite the specific
passage you drew each point from so I can confirm you didn't drift, and flag anything the note
doesn't actually support rather than smoothing over it.

Success = a paragraph I can drop in with every claim traceable to a line in the source.
```
`assumed: source-bounded to that one note; read-back via citations (no automated check — success is my read); no plan-gate.`

## Handoff — when Nile says "ok do it"

His go-ahead **satisfies the plan-approval gate** in the prompt you just wrote — do not re-ask the
same approval (that's the round-trip the skill exists to kill). Still honor any *destructive /
per-batch* gate inside it, and carry the `assumed:` defaults forward rather than re-deriving them.
The "me/I" in the forged prompt refers to Nile even though you're the one executing it.

## Guardrails

- **You draft; you don't execute.** If he says "ok do it," that's a normal execution turn (see Handoff).
- **Don't over-interrogate.** Draft first, default the rest visibly, ask only the 3+-guess exception.
- **One rec, not a slate** — one strong prompt, refined; not three variants to pick from (unless he
  asks to compare approaches, which is the one time two interpretations are right).
- **Match the stakes** — a throwaway task gets a throwaway prompt.

## Grounding

Distilled from Boris Cherny's Claude Code guidance (KB: `Media Transcripts/2026-07-23…tiktok…`
transcript + `KB/Claude/Articles + Talks/7 Ways Boris Uses Claude Code — source mirror
(2026-04-15).md`), Anthropic prompting fundamentals (be direct; give context + success criteria;
show an example of the desired output; specify format; tell it what TO do), and Nile's working style
(First Brick, terse-by-default, Plan-Mode for load-bearing work, stop-sooner, run-the-control).
