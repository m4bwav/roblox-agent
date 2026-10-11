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

## 2026-10-11 (native tools test, raw results)

- Studio MCP probe on Place1 through the native `mcp__Roblox_Studio__*` tools: every `execute_luau` sandbox probe (Edit, Server, Client) returned `G=table | createScript=true`. `script_read` after `multi_edit` read back `print("probe v2")` straight away. The console showed `probe v2` during play. Cleanup returned `found=true | remaining=0 | children=1`; the remaining child, `DestroyHelperUI` (Script), was in ServerScriptService before the run and was left alone.

Related: [INDEX.md](INDEX.md)
