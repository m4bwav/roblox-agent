# Changelog: roblox-agent-cloud

Every change to [SKILL.md](SKILL.md) and its companions, newest first, each with the reason. Reasons cite findings in [RESEARCH.md](RESEARCH.md) (`R-`), lessons in [LEARNINGS.md](LEARNINGS.md) (`L-`), and test runs in [TESTS.md](TESTS.md) (`T-`). State in `evergreen.json`. Protocol: MAINTENANCE.md.

Entry shape: `### C-YYYYMMDD-n · date · one-line summary`, then `because:` (IDs or "user request"), `files:` (file and section), and a sentence on what changed. Cite section headings, not line numbers.

### C-20261010-2 · 2026-10-10 · Help text for every subcommand and option
- because: the 0.1.1 wiki run (gap 2): `run --help` and `publish --help` listed flags with no descriptions
- files: scripts/rbx_cloud.py (main), tests/test_scripts.py
- Each subcommand and option now has a help line, tested.

### C-20261010-1 · 2026-10-10 · Created as an evergreen unit
- because: user request
- files: SKILL.md, RESEARCH.md, LEARNINGS.md, evergreen.json (skills: also TESTS.md and evals/evals.json)
- Initial version. Tier `fast`, interval 14d. See R-20261010-1 for the research basis; the first test run, for a skill, is logged in TESTS.md.
