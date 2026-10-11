# Log

Append-only. Newest last.

## 2026-10-10

- Researched Roblox and AI agents on four tracks (subject: platform and AI; tooling; practice; testing, with the toolchain installed and checked on Windows 11).
- Found that Roblox shipped a built-in Studio MCP server, an official agent plugin (2026-10-07) and in-Studio skills, so the suite was designed as the layer around them (see decisions/).
- Wrote the five skills, `rbx_check.py` (proven on a fixture place and a broken copy) and `rbx_cloud.py` (proven against a fake Open Cloud server), CI, the size budget and the release workflow. Published as v0.1.0.

- Later on 2026-10-10: added the README banner, probed the Studio MCP server live (L-001 in roblox-agent-studio), released v0.1.1, and wrote and published the wiki (verified against v0.1.1; note in notes/2026-10-10-wiki-run/).

## 2026-10-11

- PR #1 merged; tagged v0.1.2 (release workflow passed). Updated the wiki for 0.1.2 in wikiwright's Update mode: the verify run changed only the three expected cases; all checks and `live` passed (wiki commit 230a387).
- Checked the cost of the owed live runs: Studio, Open Cloud keys and Luau Execution need no payment. Found a DevForum report of an undocumented Luau Execution limit (about 30 creates an hour); it is a lead in HANDOFF.

## 2026-10-11 (live Studio test)

- First live run of roblox-agent-studio against Studio 0.742 on the dev machine, through a stdio probe of `mcp.bat` (the session predated the `claude mcp add`). 30 tools, one studio listed, playtest loop passed. `list_roblox_studios` returns `id`, not `studio_id`. The `execute_luau` sandbox reported for 0.741 did not show in Edit mode. Assistant sits behind a top-right button in the 2026 layout. Skill updated (C-20261011-1), contradiction flagged for the next refresh.

## 2026-10-11 (native tools test)

- Ran roblox-agent-studio through the native `mcp__Roblox_Studio__*` tools in a headless `claude -p` session (T-20261011-2): list, create, `multi_edit` with read-back, playtest, sandbox probe in Edit, Server and Client, cleanup. All passed; no sandbox anywhere. The interactive VS Code session had no tools because it opened the folder with a lower-case drive letter while the local-scope entry sits under the upper-case path (L-004). `execute_luau` returns only its first value (L-005). Skill updated (C-20261011-2).
- Refreshed roblox-agent-studio (R-20261011-3): Roblox staff rolled the execute_luau sandbox back on 2026-10-02, after a first rollback on 2026-09-18; it is a server-side flag that may return. Sandbox rule rewritten, eval case outcome-2 added, contradiction flag cleared (C-20261011-3).

## 2026-10-11 (native tools test, raw results)

- Studio MCP probe on Place1 through the native `mcp__Roblox_Studio__*` tools: every `execute_luau` sandbox probe (Edit, Server, Client) returned `G=table | createScript=true`. `script_read` after `multi_edit` read back `print("probe v2")` straight away. The console showed `probe v2` during play. Cleanup returned `found=true | remaining=0 | children=1`; the remaining child, `DestroyHelperUI` (Script), was in ServerScriptService before the run and was left alone.

## 2026-10-11 (PR #5 merged, studio skill trimmed)

- PR #5 conflicted with PR #4 only in this log (the raw-results bullet was in both); merged main into the branch keeping one copy, CI passed, merged at the owner's request.
- Trimmed roblox-agent-studio SKILL.md from 2,748 to 2,465 tokens (budget back to GREEN) by moving the troubleshooting list and the other-servers detail to references/troubleshooting-and-servers.md (C-20261011-4). trigger-2 and the new outcome-2 passed on the trimmed copy (T-20261011-3). Plugin bumped to 0.1.3, untagged until the PR merges.
- The "banners still missing" list in the private next-session prompt was stale: unity-agent, wikiwright, chartwright, threewright, readwright, skill-tidy, context-health and everscout all already have `.github/images/banner.jpg` and a README banner line (checked on GitHub).

## 2026-10-11 (live Open Cloud run, v0.1.3 released)

- PR #6 was merged; tagged v0.1.3, release workflow passed, release live.
- First real Open Cloud run with a scoped key on a private test experience (T-20261011-1 and R-20261011-1 in roblox-agent-cloud): Luau Execution results and logs match the skill; error tasks give FAILED with SCRIPT_ERROR; Saved upload returned versions 4 and 5. Uploads got 409 "Server is busy" while Studio had the place open (L-002). Jest Roblox 3.20.1 (`roblox/jest`, L-003) passed 2/2 once the test place set LoadStringEnabled (L-001). The DevForum "30 creations an hour" lead did not reproduce: 40 in 10 minutes were accepted. Skill and run-jest.luau fixed (C-20261011-1); plugin 0.1.4.
- Toolchain on the dev machine: Rokit 1.2.0 (self-installed to the user profile), Rojo 7.7.1 and Wally 0.3.2 as global tools.

Related: [INDEX.md](INDEX.md)
