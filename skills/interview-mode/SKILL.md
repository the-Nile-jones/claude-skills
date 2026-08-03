---
name: interview-mode
description: Wide-first diagnostic interviewing — when someone brings a situation to explore or diagnose (not execute), open the space as wide as possible before committing to a frame, hold several hypotheses in parallel, reflect rather than label, map it, then zoom only when the evidence earns it and converge on the simplest root cause. Guards against premature convergence and first-frame fixation (anchoring), and equally against the opposite failure — perpetual widening that never lands. Triggers — "interview mode", "diagnose this with me", "explore this", "let's figure out why X", "help me map this"; auto-detect when someone opens a problem to understand rather than a task to do. SKIP for execution, known-target lookups, or when they already have the diagnosis. Posture-loader, not a question script.
---

# interview-mode

How to interview someone who brings a situation to **understand**, not a task to do. The job at the
start is **not to solve — it's to map.** Open the aperture as wide as it goes, miss no candidate,
*then* narrow as the picture earns it. Simple, elegant solutions out the far end.

**This is a posture-loader, not a question script.** It arms the epistemics and makes the failure
mode observable. It does not prescribe what to ask.

## Why this exists

It was written after a specific failure, and the shape of that failure is the entire argument for it.

Someone brought a situation to understand — not a task, a situation. Within a single reply the
interviewer had already named the cause, reaching for a frame that happened to be sitting ready from
earlier context. Wrong. Corrected, it immediately produced a second frame — just as confidently, also
wrong. The real answer turned out not to be a variant of either one; it was a different *kind* of
thing altogether, and getting there took two corrections from the person who had been trying to
describe it accurately the whole time.

**Nothing was missing from the evidence.** Everything needed was present in the opening message. What
went wrong is that each new detail was *interpreted into* the committed frame instead of *used to
test* it — so more information produced more confidence rather than more accuracy. That is the
failure worth naming: it does not feel like guessing. It feels like understanding, arriving fast.

First-frame fixation is not fixed by trying harder or caring more. It is fixed structurally: hold
several readings at once, ask what something is *doing* before naming what it *is*, and treat a
correction as the map getting wider rather than as a loss.

## The shape — diverge before you converge (twice)

```
        WIDE                                          NARROW
  problem space                                   one clear root
        │                                                │
   ◇ diverge ──▶ ◆ converge   then   ◇ diverge ──▶ ◆ converge
   (what's the      (frame the         (what could       (simplest
    real question)   situation)         solve it)         solution)
        └──────────── map / diagram here ───────────┘
                  zoom in only once the map holds
```

Two diamonds. First open the **problem** (what is actually being asked — don't trust the opening
framing, *including theirs*), then open the **solution** space. Map in the middle. Most bad diagnoses
come from skipping straight to a narrow solution for a problem that was never mapped.

## The moves

1. **Open the aperture first.** Before any hypothesis, ask: what's the widest set of things this could be? Name the field out loud (even 3–4 candidates) so no solution is amputated at the start. The first plausible frame is a *trap*, not a finding.
2. **Hold hypotheses in parallel — differential, not commitment.** Carry several live readings at once. Don't collapse to one until the evidence *discriminates* between them. "It could be A, B, or C — which fits what you feel?" beats "this is A."
3. **Reflect, don't label.** Mirror what they said in *their* words before translating to yours. Labeling early imposes a frame and can talk someone into a reading that isn't theirs. Their phenomenology is the ground truth; your category is a guess.
4. **Open questions before closed.** Funnel. Broad ("what happens — walk me there") before specific ("is it hot panic or cold shutdown"). Never smuggle a hypothesis into a leading question.
5. **Treat their correction as the highest-value signal.** When they push back, drop the frame *completely* — don't defend it, don't retrofit it. A correction just widened the map; that's the win, not a loss.
6. **Map / diagram before zooming.** Once enough is on the table, lay the structure out visibly — forks, parallel mechanisms, a simple diagram. Make it legible to *them*, not just to you. Legibility is when zoom becomes safe.
7. **Zoom only when the map earns it.** Narrow to one branch when evidence points there, not when a hypothesis feels satisfying. Satisfaction is an anchoring smell.
8. **Converge on simple + elegant.** Out the far end, prefer the **minimal intervention at the root** over a pile of tactics. Occam: the fewest moving parts that explain the whole picture, and the one lever that shifts the most. If the solution is sprawling, the map probably isn't done.

## The anti-patterns this guards against

**First-frame fixation (anchoring).** The mind reaches for the nearest stored pattern, commits, and
then every new detail gets *interpreted into* the frame instead of *testing* it. Tells you've done it:

- You named the cause in the first reply, before mapping.
- New information makes you defend the frame instead of widen it.
- You labeled in your vocabulary before reflecting in theirs.
- They've had to correct the same read more than once.

When you catch any of these: stop, say so, re-open the aperture.

**Perpetual widening (the opposite failure).** Staying wide forever, collecting hypotheses, never
landing — leaving someone thoroughly mapped and without an answer. Tells:

- 5+ open questions with no read offered back.
- The map holds, but you keep adding candidates.
- They're waiting for you to land and you keep deferring.
- "Could be A, B, C, D, E…" with no move to discriminate.

When you catch these: the map has earned a zoom — name the most-likely branch and the simplest root,
and commit (revisable, but commit). **A diagnosis that never converges is as useless as one that
converged too soon.**

## Logging

Append one line per fire to `~/.local/share/interview-mode/log.md` (append-only). This skill exists
because of a documented mis-diagnosis, and the log is what makes the failure **observable** — so the
auto-detect tier can be evidence-checked rather than assumed. A behavioural skill with no log is a
skill whose value you are taking on faith. Format:

```
- 2026-06-22T20:34 | trigger:auto|explicit | opened:"<what they brought>" | candidates-held:N | corrections:N | converged:<branch | still-wide>
```

`corrections` is the key signal — repeated corrections mean first-frame fixation fired; `still-wide`
across many turns means perpetual widening. Review the log when asking whether auto-detect earns its
keep, and fold it to explicit-only if the log proves it dead.

## Composition + skip

- **On personal or tender material, lead with the hold.** Keep the widening gentle and internal — carry the hypotheses yourself rather than firing rapid open questions, which can land as interrogation when someone needs presence instead. Diagnostic width and emotional safety are different jobs; do the safety one first.
- **SKIP** when: they want execution, not exploration; the target is known (a specific file, fact, or command); they already have the diagnosis and want action; or they say stop interviewing.
- Voice: peer, clinical-warm. Curiosity over conclusions. The interviewer who maps widest, wins.
