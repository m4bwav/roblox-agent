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

### L-001 · 2026-10-11 · Smooth terrain draws its surface half a voxel above a linear occupancy; shift it, then carve only a little
- Trigger: a place generated with Lune (`@lune/roblox`, `serializePlace`) from map data: terrain voxels cannot be written there, so a builder module made the terrain with `WriteVoxels` in Studio, occupancy `(h - voxelBottom) / 4`. Paths, pads and a new asphalt street surface laid at the height-map height sat under the rendered ground; a 2-stud carve under the street still left terrain 0.1 stud above the asphalt. A calibration patch (full voxel, then occupancy o, then air, raycast the middle) measured the surface at voxel bottom + 2 + 4 * o, exactly linear, so every column drew 2 studs above its height.
- Hypothesis: Roblox treats occupancy as centred on the voxel, not filling it from the bottom.
- Rule: ship terrain as data plus a builder (bake once in Studio, and build at server start if missing), and write occupancy as `clamp((h - voxelBottom) / 4 - 0.5, 0, 1)` so the drawn surface lands on h. Then parts placed at the height-map height sit on the ground: carve only 0.4 to 0.8 studs under hard surfaces, about half a voxel past the edge, and hide the edge with a curb or border part. Check with a raycast against Terrain (part top minus terrain height) before looking at screenshots.
- Evidence: live session 2026-10-11 (before the fix: heightmap 10.06, drawn 12.12; after: drawn 11.28 under asphalt at 12.04); calibration 0.0 to 1.0 in steps of 0.1, every step +0.40 stud
- Scope: global
- Status: active · helpful 2 · harmful 0 · last_confirmed 2026-10-11

### L-001 · 2026-10-10 · One-line lesson in plain words
- Trigger: what happened, with dates or counts
- Hypothesis: why
- Rule: the shortest instruction that prevents the trigger
- Evidence: C-20261010-1, T-20261010-1, confirmed 2026-10-10
- Scope: skill | repo:<slug> | env:<name> | global
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-10
-->
