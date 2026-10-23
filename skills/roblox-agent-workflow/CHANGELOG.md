# Changelog: roblox-agent-workflow

Every change to [SKILL.md](SKILL.md) and its companions, newest first, each with the reason. Reasons cite findings in [RESEARCH.md](RESEARCH.md) (`R-`), lessons in [LEARNINGS.md](LEARNINGS.md) (`L-`), and test runs in [TESTS.md](TESTS.md) (`T-`). State in `evergreen.json`. Protocol: MAINTENANCE.md.

Entry shape: `### C-YYYYMMDD-n · date · one-line summary`, then `because:` (IDs or "user request"), `files:` (file and section), and a sentence on what changed. Cite section headings, not line numbers.

### C-20261023-1 · 2026-10-23 · Step 1: design before code, with a game-design reference
- because: owner request (book-learnings track 9, after Rogers, *Level Up!*); R-20261023-1; T-20261023-1
- files: SKILL.md (description, new Step 1, old Steps 1-8 renumbered 2-9, Output), references/game-design.md (new), evals/evals.json (trigger-3, trigger-4, decoy-3, action-2, outcome-2), RESEARCH.md
- A new experience or gameplay feature is planned before Luau: a one-pager in the repo, one metrics ModuleScript read from the place's own StarterPlayer and Workspace values, enemy cards, owner-only debug commands, multiplayer map and fairness rules, and a playtest protocol (agent break-it pass plus a human checklist). The description names game design and three new trigger phrases; evals re-run.

### C-20261017-2 · 2026-10-17 · Reference: 3D models from the developer's side
- because: user request: each plugin carries 3D modelling knowledge for its topic and points to polywright; R-20261017-1
- files: references/3d-models.md (new), SKILL.md Step 5, RESEARCH.md (Current understanding, Search plan, Findings log)
- New reference on styles, mesh limits, PBR maps, scale and pivots, collision versus rendering, performance, R15 rigs, accessories and UGC validation, Studio versus Blender, and Open Cloud model uploads; it links polywright's contract and its Roblox finishing page. Step 5 gains one pointer sentence. No trigger or decision change, so the evals were not re-run.

### C-20261017-1 · 2026-10-17 · Pointer to polywright for meshes
- because: user request (polywright HANDOFF owed item 6: siblings call polywright through the folder contract)
- files: SKILL.md Step 5
- One sentence: when a mesh is needed and polywright is installed, ask it through its asset-folder contract with the `game-roblox` target and take the file from `out/` named in `manifest.json`.

### C-20261011-4 · 2026-10-11 · Learning L-001 rewritten: the terrain surface sits half a voxel high
- because: L-001
- files: LEARNINGS.md
- Calibrated the occupancy-to-surface mapping; the fix is a half-voxel shift in the builder, and the old deep-carve rule is replaced by a shallow one.

### C-20261011-3 · 2026-10-11 · Learning: re-mesh stale terrain instead of regenerating it
- because: L-002
- files: LEARNINGS.md
- Sky-coloured holes seen only up close after repeated terrain rebuilds.

### C-20261011-2 · 2026-10-11 · Learning: Lune and terrain, carving under parts
- because: L-001
- files: LEARNINGS.md
- First real entry, from generating a map-based place.

### C-20261010-2 · 2026-10-10 · Cite the mover-constraints page for the body-mover replacements
- because: T-20261010-2 (action-1 found BodyVelocity.md tagged Deprecated without naming LinearVelocity)
- files: SKILL.md Step 2
- Added the docs page that names the replacements, so a reply can cite a source for the table rather than the skill.

### C-20261010-1 · 2026-10-10 · Created as an evergreen unit
- because: user request
- files: SKILL.md, RESEARCH.md, LEARNINGS.md, evergreen.json (skills: also TESTS.md and evals/evals.json)
- Initial version. Tier `moderate`, interval 30d. See R-20261010-1 for the research basis; the first test run, for a skill, is logged in TESTS.md.
