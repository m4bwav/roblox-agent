# Learnings: roblox-agent-studio

Procedural lessons for [SKILL.md](SKILL.md). Research findings live in [RESEARCH.md](RESEARCH.md); every change is logged in [CHANGELOG.md](CHANGELOG.md); test runs in [TESTS.md](TESTS.md); state in `evergreen.json`. Format and write-time gate: MAINTENANCE.md (LEARNINGS-FORMAT). Retired entries go to LEARNINGS-ARCHIVE.md with a reason.

Write an entry the moment a real signal happens: a user correction, the same error twice, a discovered workaround, an environment fact, a stated preference, a failed test or a failure in use. Check existing entries first, by meaning (`evergreen.py search "<the lesson>" --kinds learnings` finds near-duplicates in every registered unit): add / update / retire / none. Trigger and Hypothesis are required. Promote after three confirmations; retire when harmful > helpful.

## Active

### L-001 · 2026-10-10 · An empty tool list means no Studio has attached, not a broken server
- Trigger: first live probe on the development machine (Studio 0.742 open on its start page, MCP setting not yet turned on). `StudioMCP.exe` from the Studio version folder answered `initialize` ("Studio MCP Proxy - bridges MCP clients with Roblox Studio", tools `listChanged: true`), logged "Timed out waiting for tools to become available", returned 0 tools from `tools/list`, and `list_roblox_studios` returned `{"studios":[]}`. `%LOCALAPPDATA%\Roblox\mcp.bat` did not exist yet.
- Hypothesis: the proxy publishes Studio's tools only after a Studio with the setting on and a place open connects to it, then signals `listChanged`; `mcp.bat` is written when the setting is first enabled.
- Rule: when a client shows the Roblox server connected but with no tools, or `list_roblox_studios` is empty, check in this order: a place is open (not the start page), the MCP setting is on, then restart the client. Do not reinstall or re-register. Until `mcp.bat` exists, `<Studio version folder>\StudioMCP.exe` is the same server for a probe.
- Evidence: SKILL.md Step 5 (first checks); RESEARCH.md R-20261010-6
- Scope: global (Windows; macOS unverified)
- Status: active · helpful 0 · harmful 0 · last_confirmed 2026-10-10

### L-003 · 2026-10-11 · list_roblox_studios names the field id; the other tools call it studio_id
- Trigger: first live connection; the skill told the agent to read a `studio_id` from the list, which has none.
- Hypothesis: the list returns `{"id","name"}` and every other tool's schema asks for `studio_id`.
- Rule: take `id` from `list_roblox_studios` and pass it as `studio_id`. A Claude Code session started before `claude mcp add` does not load the tools; probe over stdio or restart.
- Evidence: T-20261011-1, T-20261011-2
- Scope: global
- Status: active · helpful 2 · harmful 0 · last_confirmed 2026-10-11

### L-004 · 2026-10-11 · A local-scope MCP entry is keyed by the exact path, drive-letter case included
- Trigger: `Roblox_Studio` was registered at local scope for `D:/work/project`; a VS Code session opened as `d:\work\project` listed no Roblox server and loaded no tools, while `claude mcp list` run from the upper-case path showed it connected.
- Hypothesis: Claude Code stores local-scope servers under the project path string in `~/.claude.json` and matches it case-sensitively on Windows; VS Code can hand over a lower-case drive letter.
- Rule: when the Studio tools are missing, run `claude mcp list` from the session's own working directory and compare the path under `projects` in `~/.claude.json`. Fix by starting the session from the same-case path, or register at project scope (`.mcp.json`). A headless `claude -p --allowedTools mcp__Roblox_Studio` from the right path also works.
- Evidence: T-20261011-2
- Scope: global (Windows)
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-11

### L-005 · 2026-10-11 · execute_luau returns only the first return value
- Trigger: `return game.Name, game.PlaceId, ...` came back as `Place1` alone.
- Hypothesis: the tool stringifies the first value of the chunk's results.
- Rule: build one string (`string.format` or `table.concat`) and return that.
- Evidence: T-20261011-2
- Scope: global
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-11

### L-002 · 2026-10-11 · In the 2026 Studio layout, Assistant is a top-right button, not a View menu item
- Trigger: the user looked under View for Assistant and found nothing; it was a button at the top right next to Collaborate.
- Hypothesis: the 2026 UI (menus File, Edit, View, Plugins, Test, Window, Help) moved Assistant out of the menus.
- Rule: send users to the top-right Assistant button with a place open, then `...` and the MCP servers setting.
- Evidence: user screenshot and report 2026-10-11
- Scope: global (Windows; macOS unverified)
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-11

<!-- Example (delete once you have a real entry):
### L-001 · 2026-10-10 · One-line lesson in plain words
- Trigger: what happened, with dates or counts
- Hypothesis: why
- Rule: the shortest instruction that prevents the trigger
- Evidence: C-20261010-1, T-20261010-1, confirmed 2026-10-10
- Scope: skill | repo:<slug> | env:<name> | global
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-10
-->
