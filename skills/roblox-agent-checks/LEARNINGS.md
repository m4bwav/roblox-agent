# Learnings: roblox-agent-checks

Procedural lessons for [SKILL.md](SKILL.md). Research findings live in [RESEARCH.md](RESEARCH.md); every change is logged in [CHANGELOG.md](CHANGELOG.md); test runs in [TESTS.md](TESTS.md); state in `evergreen.json`. Format and write-time gate: MAINTENANCE.md (LEARNINGS-FORMAT). Retired entries go to LEARNINGS-ARCHIVE.md with a reason.

Write an entry the moment a real signal happens: a user correction, the same error twice, a discovered workaround, an environment fact, a stated preference, a failed test or a failure in use. Check existing entries first, by meaning (`evergreen.py search "<the lesson>" --kinds learnings` finds near-duplicates in every registered unit): add / update / retire / none. Trigger and Hypothesis are required. Promote after three confirmations; retire when harmful > helpful.

## Active

### L-001 · 2026-10-11 · The type check passes properties that throw when a script writes them
- Trigger: `luau-lsp analyze` with the Roblox definitions passed a builder that set `workspace.Terrain.Decoration = true`; at run time it threw "Decoration is not a valid member of Terrain" and stopped the whole terrain build, so the place played with no ground.
- Hypothesis: the definitions list some properties scripts cannot write (Studio-only or not scriptable), so static checks cannot catch them.
- Rule: after the static checks, run new engine-facing code once in Studio (`execute_luau` in Edit) or a playtest and read `get_console_output` before calling it done; treat a clean type check as necessary, not sufficient.
- Evidence: live session 2026-10-11 (rbx_check all pass; console error in Play)
- Scope: global
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
