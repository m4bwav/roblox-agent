# Handoff

Last updated 2026-10-11.

## State

- v0.1.0: five skills (studio, project, checks, cloud, workflow), two scripts with 10 passing tests, CI on three operating systems plus a real-toolchain job, a size budget, and a release workflow.
- Research basis: a four-track pass on 2026-10-10, distilled into each skill's RESEARCH.md.
- v0.1.1 (2026-10-10): the studio skill's first live probe (server runs, 0 tools until a Studio with a place attaches) and the README banner.
- Wiki live at https://github.com/m4bwav/roblox-agent/wiki (10 pages, verified against v0.1.1); how to update it: [notes/2026-10-10-wiki-run/2026-10-10-github-wiki.md](notes/2026-10-10-wiki-run/2026-10-10-github-wiki.md).
- Eval runs: action and outcome cases for all five skills passed once each (T-20261010-2 in each TESTS.md).

- v0.1.2 (2026-10-11): `--defs` missing file is a usage error, `rbx_cloud.py` help text, narrower project description. Wiki updated for it the same day (wiki note, "Update for 0.1.2").
- Cost rule: the maintainer pays Roblox nothing. Studio, Open Cloud keys and Luau Execution are free; every owed run must stay on that path.
- The next session's prompt is kept in the owner's private notes, outside the repository.

## Owed

1. Live Studio test done 2026-10-11 (T-20261011-1): connection, playtest loop, sandbox not reproduced on 0.742. Still owed: a run through a registered Claude Code entry in a fresh session (tools in the trace, not a stdio probe), `multi_edit` with a read-back, and whether the sandbox applies in Server or Client data models.
2. Run `rbx_cloud.py run` and `publish --type Saved` against a real test place with a scoped key, and `references/run-jest.luau` with Jest Roblox 3.20. Confirm the `output.results` shape.
3. Run the eval suites three times per case (the first pass ran fewer; see each TESTS.md).
4. Re-check whether `/plugin` in Claude Code finds Roblox's "Roblox Studio" plugin (open question in roblox-agent-studio).
5. Lead from the DevForum (late September 2026 bug report): Luau Execution may allow only about 30 task creates an hour per key owner, beside the documented 5 a minute. Check it in the run in item 2 and add it to roblox-agent-cloud if true.
6. Consider submitting the plugin to the Anthropic plugin directory once items 1 and 2 pass.

Related: [INDEX.md](INDEX.md)
