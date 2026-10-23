# Tests: roblox-agent-workflow

Test runs for [SKILL.md](SKILL.md). Cases live in `evals/evals.json`. A failure that taught something is a lesson in [LEARNINGS.md](LEARNINGS.md); a fix it caused is logged in [CHANGELOG.md](CHANGELOG.md) with `because: T-...`; research it triggered is in [RESEARCH.md](RESEARCH.md); counts and the failing list are in `evergreen.json` under `tests`. Rules: MAINTENANCE.md (testing section) and the plugin's `protocol/TESTING.md`.

A test passes on evidence (a tool call in the trace, a file, a marker, a log line), never on the transcript's claim that something was done.

Entry shape: `### T-YYYYMMDD-n · date · harness · env · passed/total`, then one line per failing case (`id · kind · class · what the evidence showed`), then `led to:` (L-, C-, R- ids or none). Newest first. Budget 150 lines; archive older runs to `TESTS-ARCHIVE.md`.

## Runs

### T-20261023-1 · 2026-10-23 · headless claude -p (sonnet), --setting-sources project,local, --plugin-dir on the books-9 worktree, each run in its own empty folder · Windows 11 dev machine, no Studio · 26/27
- New: trigger-3 3/3, trigger-4 3/3, decoy-3 3/3, action-2 3/3 (docs/ONE-PAGER.md with the core loop and a Metrics module that the stage code requires; two runs cited the docs pages for the defaults), outcome-2 3/3 (break-it pass and human questions).
- Re-run after the description change: trigger-2 3/3, decoy-1 3/3 (roblox-agent-project chosen), decoy-2 3/3; trigger-1 2/3. trigger-1 · trigger · prompt · the prompt carries no code, and one run asked for the script before choosing a skill; the case predates this change.
- Baselines (no plugin, empty folder): action-2 0/1 (a config module with stage data, no movement numbers, no one-pager), outcome-2 0/1 (a general checklist with neither out-of-bounds play nor questions for testers).
- led to: C-20261023-1, L-003

### T-20261010-3 · 2026-10-10 · evergreen-tester subagents (one trigger case and one decoy, one run each) · Windows 11 dev machine, Claude Code · 2/2
- trigger-2 pass (no file written), decoy-2 pass (no roblox-agent skill for an Express.js review)
- led to: none

### T-20261010-2 · 2026-10-10 · evergreen-tester subagents (action and outcome cases, one run each) · Windows 11 dev machine, Claude Code, no Roblox Studio installed · 2/2
- action-1 pass (skill invoked; fetched BodyVelocity.md and deprecated.md from create.roblox.com and cited both; noted the class page does not name the replacement)
- outcome-1 pass (flagged that the client chooses the amount; server-side catalog price, type and range checks, cooldown, balance check)
- One run per case, not the suite's three; trigger and decoy cases not run separately (both action cases invoked the skill first). No baseline without the skill yet, so `worth` stays UNPROVEN.
- led to: C-20261010-2

### T-20261010-1 · 2026-10-10 · not yet run · skill · 0/0
- Suite scaffolded; no run recorded. Write the cases in `evals/evals.json` (at least two trigger prompts, two decoys, one action case with evidence, one outcome case), run the baseline without the skill, then run with it (`evergreen-test`).
- led to: none
