# Handoff

Last updated 2026-10-10.

## State

- v0.1.0: five skills (studio, project, checks, cloud, workflow), two scripts with 10 passing tests, CI on three operating systems plus a real-toolchain job, a size budget, and a release workflow.
- Research basis: a four-track pass on 2026-10-10, distilled into each skill's RESEARCH.md.

## Owed

1. Run `roblox-agent-studio` against a live Roblox Studio (none was installed on the development machine): connection, `list_roblox_studios`, the playtest loop, the `execute_luau` sandbox claim. Log results in its TESTS.md and LEARNINGS.md.
2. Run `rbx_cloud.py run` and `publish --type Saved` against a real test place with a scoped key, and `references/run-jest.luau` with Jest Roblox 3.20. Confirm the `output.results` shape.
3. Run the eval suites three times per case (the first pass ran fewer; see each TESTS.md).
4. Re-check whether `/plugin` in Claude Code finds Roblox's "Roblox Studio" plugin (open question in roblox-agent-studio).
5. Consider submitting the plugin to the Anthropic plugin directory once items 1 and 2 pass.

Related: [INDEX.md](INDEX.md)
