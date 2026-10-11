# Changelog: roblox-agent-studio

Every change to [SKILL.md](SKILL.md) and its companions, newest first, each with the reason. Reasons cite findings in [RESEARCH.md](RESEARCH.md) (`R-`), lessons in [LEARNINGS.md](LEARNINGS.md) (`L-`), and test runs in [TESTS.md](TESTS.md) (`T-`). State in `evergreen.json`. Protocol: MAINTENANCE.md.

Entry shape: `### C-YYYYMMDD-n · date · one-line summary`, then `because:` (IDs or "user request"), `files:` (file and section), and a sentence on what changed. Cite section headings, not line numbers.

### C-20261010-2 · 2026-10-10 · Step 5: an empty tool list points at Studio's state; where the binary lives
- because: R-20261010-6, L-001
- files: SKILL.md Step 5
- First live probe showed 0 tools and no studios with Studio on its start page; the troubleshooting order now says so, and notes that `mcp.bat` appears only after the setting is enabled.

### C-20261010-1 · 2026-10-10 · Created as an evergreen unit
- because: user request
- files: SKILL.md, RESEARCH.md, LEARNINGS.md, evergreen.json (skills: also TESTS.md and evals/evals.json)
- Initial version. Tier `fast`, interval 14d. See R-20261010-1 for the research basis; the first test run, for a skill, is logged in TESTS.md.
