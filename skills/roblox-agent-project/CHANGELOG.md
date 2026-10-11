# Changelog: roblox-agent-project

Every change to [SKILL.md](SKILL.md) and its companions, newest first, each with the reason. Reasons cite findings in [RESEARCH.md](RESEARCH.md) (`R-`), lessons in [LEARNINGS.md](LEARNINGS.md) (`L-`), and test runs in [TESTS.md](TESTS.md) (`T-`). State in `evergreen.json`. Protocol: MAINTENANCE.md.

Entry shape: `### C-YYYYMMDD-n · date · one-line summary`, then `because:` (IDs or "user request"), `files:` (file and section), and a sentence on what changed. Cite section headings, not line numbers.

### C-20261010-2 · 2026-10-10 · Description: luau-lsp type errors belong to roblox-agent-checks
- because: T-20261010-3 (checks trigger-2 loaded roblox-agent-project first on "why does luau-lsp say Unknown global")
- files: SKILL.md frontmatter description
- "get editor types from luau-lsp" became "set up luau-lsp for editor types", and the sibling line now sends type errors to roblox-agent-checks.

### C-20261010-1 · 2026-10-10 · Created as an evergreen unit
- because: user request
- files: SKILL.md, RESEARCH.md, LEARNINGS.md, evergreen.json (skills: also TESTS.md and evals/evals.json)
- Initial version. Tier `moderate`, interval 30d. See R-20261010-1 for the research basis; the first test run, for a skill, is logged in TESTS.md.
