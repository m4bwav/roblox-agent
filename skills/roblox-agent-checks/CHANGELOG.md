# Changelog: roblox-agent-checks

Every change to [SKILL.md](SKILL.md) and its companions, newest first, each with the reason. Reasons cite findings in [RESEARCH.md](RESEARCH.md) (`R-`), lessons in [LEARNINGS.md](LEARNINGS.md) (`L-`), and test runs in [TESTS.md](TESTS.md) (`T-`). State in `evergreen.json`. Protocol: MAINTENANCE.md.

Entry shape: `### C-YYYYMMDD-n · date · one-line summary`, then `because:` (IDs or "user request"), `files:` (file and section), and a sentence on what changed. Cite section headings, not line numbers.

### C-20261011-2 · 2026-10-11 · Learning: a clean type check does not prove engine writes work
- because: L-001
- files: LEARNINGS.md
- First real entry, from a terrain builder that type-checked but threw in Studio.

### C-20261010-2 · 2026-10-10 · A missing --defs file is a usage error
- because: the 0.1.1 wiki run (ai-docs/notes/2026-10-10-wiki-run, gap 1): `--defs missing.d.luau` skipped the types check and reported ok true with exit 0
- files: scripts/rbx_check.py (main), SKILL.md Step 1, tests/test_scripts.py
- A path the user named that does not exist now prints `{"ok": false, "error": "--defs file not found: ..."}` and exits 2.

### C-20261010-1 · 2026-10-10 · Created as an evergreen unit
- because: user request
- files: SKILL.md, RESEARCH.md, LEARNINGS.md, evergreen.json (skills: also TESTS.md and evals/evals.json)
- Initial version. Tier `moderate`, interval 30d. See R-20261010-1 for the research basis; the first test run, for a skill, is logged in TESTS.md.
