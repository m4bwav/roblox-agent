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

Related: [INDEX.md](INDEX.md)
