# Tests: roblox-agent-project

Test runs for [SKILL.md](SKILL.md). Cases live in `evals/evals.json`. A failure that taught something is a lesson in [LEARNINGS.md](LEARNINGS.md); a fix it caused is logged in [CHANGELOG.md](CHANGELOG.md) with `because: T-...`; research it triggered is in [RESEARCH.md](RESEARCH.md); counts and the failing list are in `evergreen.json` under `tests`. Rules: MAINTENANCE.md (testing section) and the plugin's `protocol/TESTING.md`.

A test passes on evidence (a tool call in the trace, a file, a marker, a log line), never on the transcript's claim that something was done.

Entry shape: `### T-YYYYMMDD-n · date · harness · env · passed/total`, then one line per failing case (`id · kind · class · what the evidence showed`), then `led to:` (L-, C-, R- ids or none). Newest first. Budget 150 lines; archive older runs to `TESTS-ARCHIVE.md`.

## Runs

### T-20261010-3 · 2026-10-10 · evergreen-tester subagents (one trigger case and one decoy, one run each) · Windows 11 dev machine, Claude Code · 2/2
- checks trigger-2 · overlap · roblox-agent-project loaded before roblox-agent-checks (the expected skill still loaded); description narrowed in C-20261010-2
- trigger-2 pass, decoy-1 pass
- led to: C-20261010-2

### T-20261010-2 · 2026-10-10 · evergreen-tester subagents (action and outcome cases, one run each) · Windows 11 dev machine, Claude Code, no Roblox Studio installed · 2/2
- action-1 pass (skill invoked; searched for *.project.json and rokit/aftman/foreman manifests, then read them, before recommending; identified Rojo and the pinned toolchain)
- outcome-1 pass (said no: one writer per script, the next sync overwrites one side; scripts on disk, MCP for non-script instances)
- One run per case, not the suite's three; trigger and decoy cases not run separately (both action cases invoked the skill first). No baseline without the skill yet, so `worth` stays UNPROVEN.
- led to: none

### T-20261010-1 · 2026-10-10 · not yet run · skill · 0/0
- Suite scaffolded; no run recorded. Write the cases in `evals/evals.json` (at least two trigger prompts, two decoys, one action case with evidence, one outcome case), run the baseline without the skill, then run with it (`evergreen-test`).
- led to: none
