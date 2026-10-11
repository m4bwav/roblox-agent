# Tests: roblox-agent-studio

Test runs for [SKILL.md](SKILL.md). Cases live in `evals/evals.json`. A failure that taught something is a lesson in [LEARNINGS.md](LEARNINGS.md); a fix it caused is logged in [CHANGELOG.md](CHANGELOG.md) with `because: T-...`; research it triggered is in [RESEARCH.md](RESEARCH.md); counts and the failing list are in `evergreen.json` under `tests`. Rules: MAINTENANCE.md (testing section) and the plugin's `protocol/TESTING.md`.

A test passes on evidence (a tool call in the trace, a file, a marker, a log line), never on the transcript's claim that something was done.

Entry shape: `### T-YYYYMMDD-n · date · harness · env · passed/total`, then one line per failing case (`id · kind · class · what the evidence showed`), then `led to:` (L-, C-, R- ids or none). Newest first. Budget 150 lines; archive older runs to `TESTS-ARCHIVE.md`.

## Runs

### T-20261011-3 · 2026-10-11 · evergreen-tester subagents on the trimmed working copy (one run each) · Windows 11 dev machine, Claude Code, no Studio running · 2/2
- trigger-2 pass: SKILL.md read, then references/troubleshooting-and-servers.md read; answer walked the moved list in order (place open, toggle, restart, reopen, one server, path case, port 13469)
- outcome-2 pass (first run): named Studio's execute_luau capability sandbox, rolled out and back by Roblox, not a refusal; proposed multi_edit or a synced file, restarting Studio and checking the DevForum; said not to override feature flags. Regex `(?i)(sandbox|capabilit)` matches; the negative FFlag regex does not.
- led to: none (confirms C-20261011-4 kept behaviour)

### T-20261011-2 · 2026-10-11 · native `mcp__Roblox_Studio__*` tools in a headless `claude -p` session (stream-json trace) started in the folder holding the local-scope entry · Windows 11 dev machine, Studio 0.742.0.7421053, unsaved template place (PlaceId 0) · 5/5
- connection pass: `list_roblox_studios` in the trace returned one studio (`Place1`); its `id` passed as `studio_id` on every later call
- edit loop pass: `execute_luau` (Edit) created `ServerScriptService.AgentProbe`; `script_read` gave `print("probe v1")`; `multi_edit` (old_string/new_string) reported "1 edits applied"; the second `script_read` gave `print("probe v2")` straight away (no stale read on a one-line script)
- playtest pass: `start_stop_play` true, `get_studio_state` Play with Client and Server; `get_console_output` showed `probe v2`, so the edited script ran
- sandbox not reproduced in any data model: Edit, Server and Client each returned `G=table | createScript=true` (pcall around creating a Script under ServerScriptService)
- cleanup pass: stop returned Edit; AgentProbe destroyed, read-back found none left
- side findings: `execute_luau` returned only the first of several return values; the interactive VS Code session (lower-case drive letter) did not load the entry registered under the upper-case path
- led to: L-004, L-005, R-20261011-2, C-20261011-2

### T-20261011-1 · 2026-10-11 · live probe, stdio client against mcp.bat (read-only, then the playtest loop on an unsaved template place) · Windows 11 dev machine, Studio 0.742.0.7421053, Claude Code manual local entry · 5/5
- connection pass: 30 tools; `list_roblox_studios` returned `{"studios":[{"id":"8d342c41-...","name":"Place1"}]}`; `get_studio_state` Edit mode
- playtest loop pass: `start_stop_play` true → "Game Started", state Play with Client and Server; `execute_luau` Server returned "1 players, gravity 196.2"; `get_console_output` showed the probe's own print; stop → Edit again
- sandbox claim not reproduced: in Edit, `_G` was a table and a new Script parented to ServerScriptService without error (then destroyed; read-back found nothing left)
- led to: L-002, L-003, R-20261011-1, C-20261011-1

### T-20261010-3 · 2026-10-10 · evergreen-tester subagents (one trigger case and one decoy, one run each) · Windows 11 dev machine, Claude Code · 2/2
- trigger-2 pass, decoy-1 pass
- led to: none

### T-20261010-2 · 2026-10-10 · evergreen-tester subagents (action and outcome cases, one run each) · Windows 11 dev machine, Claude Code, no Roblox Studio installed · 2/2
- action-1 pass (skill invoked; `claude mcp list` and the config read before any entry was proposed; no Roblox server found, mcp.bat absent, so Studio install named first)
- outcome-1 pass (named the execute_luau capability sandbox from Studio 0.741, not a refusal; proposed multi_edit with a fresh read and synced files)
- One run per case, not the suite's three; trigger and decoy cases not run separately (both action cases invoked the skill first). No baseline without the skill yet, so `worth` stays UNPROVEN.
- led to: none

### T-20261010-1 · 2026-10-10 · not yet run · skill · 0/0
- Suite scaffolded; no run recorded. Write the cases in `evals/evals.json` (at least two trigger prompts, two decoys, one action case with evidence, one outcome case), run the baseline without the skill, then run with it (`evergreen-test`).
- led to: none
