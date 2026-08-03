---
name: skill-scout
description: >-
  Recon-and-triage loop for external skill/pattern sources. Use when Nile wants to scan a skill hub, repo, marketplace, or article for new skills / skill ideas / atomic candidates / diminishing-returns — "scan for new skills", "anything new in anthropics/skills", "check the skill hubs", "mine this source for skill ideas", "what should I grab", "/skill-scout". Fetches the source live, Venn-dedups every candidate against installed skills AND the atom library FIRST, then emits three buckets: new-skill candidates, atomic candidates, already-covered (diminishing returns). It does NOT install, build, or mint atoms — those are separate gated steps it hands off to. The dedup gate is the load-bearing part; it exists because improvised scans keep skipping it and "discovering" things already owned. On-demand: suggest it, don't auto-fire.
---

# skill-scout — External Source Recon & Triage

A deterministic loop for "is there anything here worth taking?" — applied to skill repos, plugin marketplaces, cookbooks, or a single article. It exists because the same procedure kept getting hand-rolled, and the hand-rolled version **skips the dedup gate** and reports things you already own as new. (Lived example: a teaching-loop "gap" that was already atomized from the same page that day.) The gate is the whole point.

## What it produces — always these three buckets

1. **New-skill candidates** — capabilities NOT covered by an installed skill. Per candidate: one line of what it does, the closest existing skill, gap type (`none` / `partial` / `full`), and an **install-vs-build** call.
2. **Atomic candidates** — structural *principles* worth porting to the Exocortex (not whole skills). These are **flagged, not minted** — they are the *input* to `/pattern-extraction`, which does the actual RMA/DMA + atom write. skill-scout never writes to the atom store itself.
3. **Already-covered / diminishing-returns** — what the source restates that you already have, each named to its covering skill or atom. **This bucket is the deliverable, not the leftover** — it's the signal that tells you a vein is mined so you stop spending energy on it.

## The loop

### 1. Identify, classify, and ground

Three things before fetching anything substantive:

- **Owned or community?** Anthropic-owned sources (`github.com/anthropics/skills`, `anthropics/anthropic-cookbook`, the Claude Docs skills pages, the `/claude-api` bundled list) carry a **low fabrication-prior**. Everything else — community marketplaces, `awesome-*` aggregators, obra/superpowers, third-party blogs — is **Tier-4**: apply source-vetting (`X-JTK-01`), strip fabricated stats and capability claims before crediting anything. Note the owner explicitly; it sets the skepticism level. **Caveat:** "trusted" lowers the prior, it does **not** exempt *falsifiable* claims (API behavior, version specifics) from verification against a primary tool like `/claude-api`. The prefill-400 claim was true but still had to be checked.
- **Already audited?** Check for a prior audit of this exact source — vault (`KB/Claude/Best Practices/*audit*`), the MA validation log, or a previous skill-scout breadcrumb. If scanned before, run in **DIFF MODE**: report only what changed since the last audit. Don't trust the prior audit blindly, though — spot-check that a few items it marked "covered" are *still* installed (an audit can outlive the reality it described).
- **Load the fit-context — non-negotiable, and the easiest step to skip.** Every "no-fit" / "install" / "build" call you'll make depends on knowing Nile's stack and what's been *evaluated-and-removed* before. A cold session that skips this will mis-triage (e.g. flag `pptx` as a candidate when slides have no workflow here). Load it from: `~/.claude/rules/skill-router.md` (the removed-skills + demoted-skills history — this is the canonical "already judged" record), `~/CLAUDE.md` (stack + canonical tools), and `ls ~/.claude/skills/`. A candidate that matches a *removed* skill goes straight to bucket 3 with the removal reason, never bucket 1.

### 2. Fetch the source live and enumerate candidates — never from memory

Pull the *current* state (`WebFetch`, or `gh api` for GitHub trees — training-data recall is stale and violates verify-before-asserting). Enumerate per source-type:

- **Repo / hub** → list the actual skill directories (`gh api repos/<o>/<r>/git/trees/<branch>?recursive=1`). GitHub's HTML file-tree is JS-rendered and won't enumerate via `WebFetch` — use the API.
- **Article / blog** → extract every concrete technique or prompt verbatim; there are no directories, the "candidates" are the techniques.
- **Marketplace** → enumerate listings; raise the vetting bar (Tier-4 by default, often unmaintained).

### 3. Pre-filter large candidate sets — and log what you cut

For a handful of candidates, skip to step 4. For a large set (a marketplace, a sprawling repo), the per-candidate gate doesn't scale — so cut obvious no-fits *by category* first (creative-coding, slides, enterprise team-comms, anything matching a removed skill from step 1). **Then state what you dropped and why** — `Pre-filtered N candidates by category: [list]`. Silent truncation reads as "scanned everything" when it didn't; an explicit drop-list keeps the cut honest and lets Nile overrule a category.

### 4. Targeted dedup gate — the load-bearing step

For each surviving candidate, query the baseline *for that candidate's domain* (don't pre-pull the whole library — targeted beats snapshot):

- Does an installed skill already do this? (you have the `ls` from step 1; read the matching skill's *description*.) → bucket 3 (name it), or bucket 1 gap=`partial` only if the candidate adds a real delta.
- Is the underlying principle already an atom? → `mcp__neo4j-cypher__read_neo4j_cypher`, matching `family` / `tags` / `statement` keywords for *this* candidate's domain. "Skill ideas" most often turn out to be principles you already hold. → bucket 3 (name the atom), or hand the *delta only* to `/pattern-extraction`.
- Absent from both? → bucket 1 (skill) or bucket 2 (atomic candidate).

Skipping this for even one candidate is how false "new" findings get through. If something "obviously" looks new — that's exactly when to run it.

**Rigor floor — ≥3×3× per atomic scan (standing rule, 2026-06-15).** The gap/diagonal verdict for an atomic scan target is not a glance — run it through at least a **3×3×** RMA/DMA pass (compose `/pattern-extraction`): 3 constructive passes decomposing what the candidate actually offers, 3 adversarial passes attacking the claim (already-covered? off-stack? survives Test-11 grounding in Nile's actual regime, not the abstract? a real delta or just a restatement of something owned?). **Upgrade up to 10×10× when the juice is worth the squeeze** — a high-value target (an official vendor skill for a daily-use in-stack tool, a plausible diagonal) earns the deeper pass; a niche/personal-tool catch-all does not. Calibrate the squeeze to the prize. (The 2026-06-15 Cloudflare eval ran ~1×1× and got lucky; this floor exists so the next verdict doesn't depend on luck.)

### 5. Triage + install-vs-build (bucket 1 only)

- **Install** when it's a packaged Anthropic/community skill or an MCP that exists and audits clean → `/mcp-install` (MCPs) or note the install path. Community installs get `/skill-security-auditor` first.
- **Build** when it's a *pattern* with no clean package, or it needs adaptation to Nile's stack → `skill-creator`.

### 6. Report + leave a dedup breadcrumb

Emit the three buckets (template below). Then append a one-line audit entry — source, date, verdict, candidate counts, and the drop-list from step 3 — where the *next* scan will check in step 1 (the capture buffer for boot-sweep, or a `KB/Claude/Best Practices/*-audit-*.md` doc for a substantial source). A scan that doesn't record itself dooms the next scan to re-mine.

## Report template

```
# skill-scout — <source> (<owned|Tier-4>) — <date> [<full scan | diff since <prior audit>>]

## New-skill candidates (N)
- <name> — <what it does>. Closest existing: <skill or "none">. Gap: <none|partial|full>. → <install | build>

## Atomic candidates (N)  → hand off to /pattern-extraction
- <principle, one line>. Closest atom: <id or "none">. Delta worth porting: <what>

## Already-covered / diminishing returns (N)
- <source item> = <covering skill/atom id>   (or: = REMOVED <skill>, <reason>)

## Pre-filtered (if any)
- <N candidates dropped by category: ...>

## Verdict
<one line: is this vein worth more passes, or mined?>
```

## Boundaries — what skill-scout does NOT do

- **Doesn't install, build, or mint.** It triages and reports. Installing (`/mcp-install`, `skill-creator`) and atom-writing (`/pattern-extraction`) are separate gated actions it hands off to — keeping recon read-only means a scan can never have a surprising side effect.
- **Division of labor with `/pattern-extraction`:** scout is *triage* — "is there anything here worth mining?" — and is read-only. pattern-extraction is *extraction* — it runs the full RMA/DMA and writes atoms. Scout's bucket-2 atomic candidates are pattern-extraction's **input**, not a duplicate of its Step 0. Run scout to decide *whether* a source is worth a pattern-extraction pass; run pattern-extraction to actually mine it. Don't run both as redundant dedups on the same source.
- **Doesn't trust Tier-4 at face value, or trusted sources blindly.** Community sources get per-claim vetting; Anthropic-owned sources still get their *falsifiable* claims checked against a primary tool.
- **Doesn't re-mine.** Already-audited source → diff mode, with a spot-check that the prior audit still holds.

## Provenance

Captures the scan-and-triage procedure run ad hoc 3× in one session (NotebookLM docs, XDA engineer prompts, skill-hubs) before being made deterministic — the skill-candidate diagonal from NILE_PATTERNS (3+ recurring repeatable procedure → route to skill-creator). Dedup discipline mirrors the `/pattern-extraction` Step-0 Duplicate Source Registry and the source-vetting atom `X-JTK-01`. Hardened via a 5×5 RMA/DMA pass 2026-06-15 (fixes: cold-session fit-context loading, fetch-before-baseline ordering, large-source pre-filter with logged drops, pattern-extraction boundary, per-source-type modes, trusted≠unverified).
