# Handoff

Last updated 2026-10-10 (late).

## State

- v0.1.0: five skills (studio, project, checks, cloud, workflow), two scripts with 10 passing tests, CI on three operating systems plus a real-toolchain job, a size budget, and a release workflow.
- Research basis: a four-track pass on 2026-10-10, distilled into each skill's RESEARCH.md.
- v0.1.1 (2026-10-10): the studio skill's first live probe (server runs, 0 tools until a Studio with a place attaches) and the README banner.
- Wiki live at https://github.com/m4bwav/roblox-agent/wiki (10 pages, verified against v0.1.1); how to update it: [notes/2026-10-10-wiki-run/2026-10-10-github-wiki.md](notes/2026-10-10-wiki-run/2026-10-10-github-wiki.md).
- Eval runs: action and outcome cases for all five skills passed once each (T-20261010-2 in each TESTS.md).

## Owed

1. Run `roblox-agent-studio` against a live Roblox Studio with a place open and the MCP setting on (the maintainer's clicks): connection, `list_roblox_studios`, the playtest loop, the `execute_luau` sandbox claim. Studio 0.742 is installed on the development machine since 2026-10-10. Log results in its TESTS.md and LEARNINGS.md.
2. Run `rbx_cloud.py run` and `publish --type Saved` against a real test place with a scoped key, and `references/run-jest.luau` with Jest Roblox 3.20. Confirm the `output.results` shape.
3. Run the eval suites three times per case (the first pass ran fewer; see each TESTS.md).
4. Re-check whether `/plugin` in Claude Code finds Roblox's "Roblox Studio" plugin (open question in roblox-agent-studio).
5. Fix the two gaps the wiki run found (`--defs` missing file reported as a skip with ok true; `rbx_cloud.py` subcommand help has no descriptions), see the wiki note.
6. Consider submitting the plugin to the Anthropic plugin directory once items 1 and 2 pass.

Related: [INDEX.md](INDEX.md)
