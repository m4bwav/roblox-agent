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

<!-- Example (delete once you have a real entry):
### L-001 · 2026-10-10 · One-line lesson in plain words
- Trigger: what happened, with dates or counts
- Hypothesis: why
- Rule: the shortest instruction that prevents the trigger
- Evidence: C-20261010-1, T-20261010-1, confirmed 2026-10-10
- Scope: skill | repo:<slug> | env:<name> | global
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-10
-->
