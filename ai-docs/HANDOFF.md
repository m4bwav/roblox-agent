# Handoff

Last updated 2026-10-18.

## State

- v0.1.0: five skills (studio, project, checks, cloud, workflow), two scripts with 10 passing tests, CI on three operating systems plus a real-toolchain job, a size budget, and a release workflow.
- Research basis: a four-track pass on 2026-10-10, distilled into each skill's RESEARCH.md.
- v0.1.1 (2026-10-10): the studio skill's first live probe (server runs, 0 tools until a Studio with a place attaches) and the README banner.
- Wiki live at https://github.com/m4bwav/roblox-agent/wiki (10 pages, verified against v0.1.1); how to update it: [notes/2026-10-10-wiki-run/2026-10-10-github-wiki.md](notes/2026-10-10-wiki-run/2026-10-10-github-wiki.md).
- Eval runs: action and outcome cases for all five skills passed once each (T-20261010-2 in each TESTS.md).

- v0.1.2 (2026-10-11): `--defs` missing file is a usage error, `rbx_cloud.py` help text, narrower project description. Wiki updated for it the same day (wiki note, "Update for 0.1.2").
- v0.1.3 (2026-10-11): roblox-agent-studio SKILL.md trimmed back to green. 0.1.4 to 0.1.6: live Open Cloud findings, listing files, learnings and 3D-model guidance; released as v0.1.6 on 2026-10-18.
- Cost rule: the maintainer pays Roblox nothing. Studio, Open Cloud keys and Luau Execution are free; every owed run must stay on that path.
- The next session's prompt is kept in the owner's private notes, outside the repository.

## Owed

1. Live Studio test done 2026-10-11 (T-20261011-1 stdio probe, T-20261011-2 native tools): connection, `multi_edit` with read-back, playtest loop; the 0.741 sandbox did not show in Edit, Server or Client on 0.742. The refresh found staff rolled it back on 2026-10-02 (R-20261011-3). Left: macOS, and the new eval case outcome-2.
2. Done 2026-10-11 (T-20261011-1 in roblox-agent-cloud): run, Saved publish and Jest 3.20.1 all passed against a real test place. Wiki owes an update for 0.1.3 and 0.1.4.
3. Run the eval suites three times per case (the first pass ran fewer; see each TESTS.md).
4. Re-check whether `/plugin` in Claude Code finds Roblox's "Roblox Studio" plugin (open question in roblox-agent-studio).
5. DevForum lead of about 30 task creates an hour: did not reproduce (40 in 10 minutes accepted, 2026-10-11). Closed.
6. Listings (2026-10-13, [notes/2026-10-13-listings.md](notes/2026-10-13-listings.md)): awesome-copilot #5063 waits for a maintainer; Cursor and the DevForum post need the owner signed in; the Claude directory is held back until his earlier submissions clear review.

Related: [INDEX.md](INDEX.md)
