# Log

Append-only. Newest last.

## 2026-10-10

- Researched Roblox and AI agents on four tracks (subject: platform and AI; tooling; practice; testing, with the toolchain installed and checked on Windows 11).
- Found that Roblox shipped a built-in Studio MCP server, an official agent plugin (2026-10-07) and in-Studio skills, so the suite was designed as the layer around them (see decisions/).
- Wrote the five skills, `rbx_check.py` (proven on a fixture place and a broken copy) and `rbx_cloud.py` (proven against a fake Open Cloud server), CI, the size budget and the release workflow. Published as v0.1.0.

Related: [INDEX.md](INDEX.md)
