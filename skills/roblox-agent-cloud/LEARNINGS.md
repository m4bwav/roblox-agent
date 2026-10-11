# Learnings: roblox-agent-cloud

Procedural lessons for [SKILL.md](SKILL.md). Research findings live in [RESEARCH.md](RESEARCH.md); every change is logged in [CHANGELOG.md](CHANGELOG.md); test runs in [TESTS.md](TESTS.md); state in `evergreen.json`. Format and write-time gate: MAINTENANCE.md (LEARNINGS-FORMAT). Retired entries go to LEARNINGS-ARCHIVE.md with a reason.

Write an entry the moment a real signal happens: a user correction, the same error twice, a discovered workaround, an environment fact, a stated preference, a failed test or a failure in use. Check existing entries first, by meaning (`evergreen.py search "<the lesson>" --kinds learnings` finds near-duplicates in every registered unit): add / update / retire / none. Trigger and Hypothesis are required. Promote after three confirmations; retire when harmful > helpful.

## Active

### L-001 · 2026-10-11 · Jest Roblox needs LoadStringEnabled in the test place
- Trigger: live run 2026-10-11: every suite failed with "loadstring() is not available" and Jest reported 0 tests; the old entry script then said "no tests found"
- Hypothesis: jest-runtime loads spec modules with loadstring, which servers refuse unless ServerScriptService.LoadStringEnabled is set
- Rule: set LoadStringEnabled in the test place's Rojo project, and treat failed suites as failures, not as zero tests
- Evidence: R-20261011-1, T-20261011-1, confirmed 2026-10-11
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-11

### L-002 · 2026-10-11 · Close the place in Studio before uploading a version
- Trigger: place-version upload returned 409 "Server is busy" twice while Studio had the place open; it worked at once after Studio closed
- Hypothesis: an open Studio session (collaborative editing) holds a lock on the place
- Rule: on that 409, ask the user to close the place in Studio, then retry; do not retry blindly
- Evidence: R-20261011-1, confirmed 2026-10-11
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-11

### L-003 · 2026-10-11 · Jest Roblox 3.20 is roblox/jest on Wally
- Trigger: `wally install` found no match for jsdotlua/jest@3.20.0
- Hypothesis: the package moved to the roblox scope; jsdotlua/jest stops at 3.10.0
- Rule: use roblox/jest and roblox/jest-globals for current versions
- Evidence: Wally index, R-20261011-1, confirmed 2026-10-11
- Scope: skill
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
