# Changelog: roblox-agent-studio

Every change to [SKILL.md](SKILL.md) and its companions, newest first, each with the reason. Reasons cite findings in [RESEARCH.md](RESEARCH.md) (`R-`), lessons in [LEARNINGS.md](LEARNINGS.md) (`L-`), and test runs in [TESTS.md](TESTS.md) (`T-`). State in `evergreen.json`. Protocol: MAINTENANCE.md.

Entry shape: `### C-YYYYMMDD-n · date · one-line summary`, then `because:` (IDs or "user request"), `files:` (file and section), and a sentence on what changed. Cite section headings, not line numbers.

### C-20261011-5 · 2026-10-11 · Learnings: proxy attach delay, driving Studio from a plain client
- because: L-006, L-007
- files: LEARNINGS.md
- Two entries from building a large place through the proxy; SKILL.md unchanged (size budget).

### C-20261011-4 · 2026-10-11 · Trim: troubleshooting list and other servers moved to a reference
- because: size budget (SKILL.md 2,748 tokens, over the 2,500 green line)
- files: SKILL.md Step 2 (item 5), Step 5, Step 6; new references/troubleshooting-and-servers.md
- No claim changed. Step 5 keeps the first three checks and points to the full ordered list; Step 6 keeps the default and the two never-use rules. SKILL.md is 2,465 tokens.

### C-20261011-3 · 2026-10-11 · Refresh: sandbox described as a rolled-back flag, eval case for its return
- because: R-20261011-3
- files: SKILL.md Step 2 (item 5), Step 3 (sandbox rule); RESEARCH.md current understanding, open questions, search plan; evals/evals.json (outcome-2)
- The sandbox is a server-side flag Roblox turned on and rolled back twice; the agent names the error, routes around it, and never suggests flag overrides. Contradiction flag cleared.

### C-20261011-2 · 2026-10-11 · Native-tool test: sandbox absent in all data models, path-case note, single return value
- because: T-20261011-2, R-20261011-2, L-004, L-005
- files: SKILL.md Step 2 (item 5), Step 3 (sandbox rule, new execute_luau rule)
- The sandbox rule now cites Edit, Server and Client; verification notes that a local-scope entry follows the exact path case; agents return one string from `execute_luau`.

### C-20261011-1 · 2026-10-11 · Live test: where the setting is, the id field, the sandbox claim softened
- because: T-20261011-1, R-20261011-1, L-002, L-003
- files: SKILL.md Step 2 (items 1 and 5), Step 3 (sandbox rule), Output
- The setting needs an open place and in the 2026 layout lives behind a top-right Assistant button; `list_roblox_studios` returns `id`, passed as `studio_id`; the 0.741 sandbox was not reproduced on 0.742, so the agent tries the direct call first.

### C-20261010-2 · 2026-10-10 · Step 5: an empty tool list points at Studio's state; where the binary lives
- because: R-20261010-6, L-001
- files: SKILL.md Step 5
- First live probe showed 0 tools and no studios with Studio on its start page; the troubleshooting order now says so, and notes that `mcp.bat` appears only after the setting is enabled.

### C-20261010-1 · 2026-10-10 · Created as an evergreen unit
- because: user request
- files: SKILL.md, RESEARCH.md, LEARNINGS.md, evergreen.json (skills: also TESTS.md and evals/evals.json)
- Initial version. Tier `fast`, interval 14d. See R-20261010-1 for the research basis; the first test run, for a skill, is logged in TESTS.md.
