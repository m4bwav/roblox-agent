# Learnings: roblox-agent-workflow

Procedural lessons for [SKILL.md](SKILL.md). Research findings live in [RESEARCH.md](RESEARCH.md); every change is logged in [CHANGELOG.md](CHANGELOG.md); test runs in [TESTS.md](TESTS.md); state in `evergreen.json`. Format and write-time gate: MAINTENANCE.md (LEARNINGS-FORMAT). Retired entries go to LEARNINGS-ARCHIVE.md with a reason.

Write an entry the moment a real signal happens: a user correction, the same error twice, a discovered workaround, an environment fact, a stated preference, a failed test or a failure in use. Check existing entries first, by meaning (`evergreen.py search "<the lesson>" --kinds learnings` finds near-duplicates in every registered unit): add / update / retire / none. Trigger and Hypothesis are required. Promote after three confirmations; retire when harmful > helpful.

## Active

### L-002 · 2026-10-11 · Rebuilding terrain several times in one session can leave flat sky-coloured patches up close
- Trigger: after five Clear-and-WriteVoxels rebuilds in one Studio session, the user saw flat blue patches (sky colour) near the camera that vanished when zoomed out. Raycasts there hit solid Grass and no part covered the spot.
- Hypothesis: Studio kept stale near-LOD terrain meshes for some chunks after the rapid rewrites; the voxel data was correct.
- Rule: if terrain shows sky-coloured holes only up close, first raycast the spot (data or rendering?); if the data is solid, read and write back the same voxels over the area (ReadVoxels then WriteVoxels, 128-stud regions) to force a re-mesh, or save and reopen the place. Do not regenerate the data.
- Evidence: live session 2026-10-11, one re-mesh pass of 304 regions cleared it
- Scope: global
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-11

### L-001 · 2026-10-11 · Lune cannot write terrain, and parts laid on smooth terrain sink unless it is carved
- Trigger: a place generated with Lune (`@lune/roblox`, `serializePlace`) from map data: terrain voxels cannot be written there, so a builder module made the terrain with `WriteVoxels` in Studio. Paths, pool decks and court pads placed at the height-map height then sat 0.3 to 0.7 studs under the rendered surface, invisible; carving a strip narrower than two 4-stud voxels did not help.
- Hypothesis: `WriteVoxels` occupancy plus smoothing puts the surface up to about a voxel off the source height, and a narrow carve is averaged back up by its neighbours.
- Rule: ship terrain as data plus a builder (bake once in Studio, and build at server start if missing). Under every part that must show on the ground, lower the height map at least one extra voxel (4 studs) beyond the part's edge and 1.5 to 2.5 studs below its top, and give the part enough thickness to hide the step. Check with a raycast against Terrain, part top minus terrain height, before looking at screenshots.
- Evidence: live session 2026-10-11 (probe: before -0.3 to -0.7 studs, after +1 to +2.8)
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
