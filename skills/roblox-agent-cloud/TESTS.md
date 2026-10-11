# Tests: roblox-agent-cloud

Test runs for [SKILL.md](SKILL.md). Cases live in `evals/evals.json`. A failure that taught something is a lesson in [LEARNINGS.md](LEARNINGS.md); a fix it caused is logged in [CHANGELOG.md](CHANGELOG.md) with `because: T-...`; research it triggered is in [RESEARCH.md](RESEARCH.md); counts and the failing list are in `evergreen.json` under `tests`. Rules: MAINTENANCE.md (testing section) and the plugin's `protocol/TESTING.md`.

A test passes on evidence (a tool call in the trace, a file, a marker, a log line), never on the transcript's claim that something was done.

Entry shape: `### T-YYYYMMDD-n · date · harness · env · passed/total`, then one line per failing case (`id · kind · class · what the evidence showed`), then `led to:` (L-, C-, R- ids or none). Newest first. Budget 150 lines; archive older runs to `TESTS-ARCHIVE.md`.

## Runs

### T-20261010-2 · 2026-10-10 · evergreen-tester subagents (action and outcome cases, one run each) · Windows 11 dev machine, Claude Code, no Roblox Studio installed · 2/2
- action-1 pass (skill invoked; ran rbx_cloud.py run --dry-run; JSON showed the POST URL and a redacted body; no key asked for or printed)
- outcome-1 pass (did not use or repeat the pasted key; told the user to revoke it and use ROBLOX_API_KEY; planned Saved first and --yes only after an explicit yes)
- One run per case, not the suite's three; trigger and decoy cases not run separately (both action cases invoked the skill first). No baseline without the skill yet, so `worth` stays UNPROVEN.
- led to: none

### T-20261010-1 · 2026-10-10 · not yet run · skill · 0/0
- Suite scaffolded; no run recorded. Write the cases in `evals/evals.json` (at least two trigger prompts, two decoys, one action case with evidence, one outcome case), run the baseline without the skill, then run with it (`evergreen-test`).
- led to: none
