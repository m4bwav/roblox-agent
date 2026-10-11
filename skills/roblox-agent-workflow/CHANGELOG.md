# Changelog: roblox-agent-workflow

Every change to [SKILL.md](SKILL.md) and its companions, newest first, each with the reason. Reasons cite findings in [RESEARCH.md](RESEARCH.md) (`R-`), lessons in [LEARNINGS.md](LEARNINGS.md) (`L-`), and test runs in [TESTS.md](TESTS.md) (`T-`). State in `evergreen.json`. Protocol: MAINTENANCE.md.

Entry shape: `### C-YYYYMMDD-n · date · one-line summary`, then `because:` (IDs or "user request"), `files:` (file and section), and a sentence on what changed. Cite section headings, not line numbers.

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
