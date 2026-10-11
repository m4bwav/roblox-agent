# Research: roblox-agent-checks

Findings that back [SKILL.md](SKILL.md). Changes they caused are logged in [CHANGELOG.md](CHANGELOG.md); procedural lessons live in [LEARNINGS.md](LEARNINGS.md); test runs in [TESTS.md](TESTS.md); schedule and state in `evergreen.json`. Protocol: MAINTENANCE.md.

Topic: verifying Roblox Luau without Studio. Tier `moderate`. Last refresh 2026-10-10; next due per `evergreen.json`.

## Current understanding

- The standard 2026 CI pipeline, from real workflows (rojo-rbx/rojo, littensy/reflex, Roblox/rodux, Quenty/NevermoreEngine and others): toolchain action (`CompeyDev/setup-rokit@v0.2.1`; older repos setup-aftman or setup-foreman), `wally install`, `rojo sourcemap`, download luau-lsp's `globalTypes.d.luau`, `luau-lsp analyze`, `selene`, `stylua --check`, `rojo build`. Engine tests in CI are the minority and go through Open Cloud Luau Execution.
- `luau-lsp analyze` (1.70.1) does not download definitions: without `--defs=globalTypes.d.luau` every Roblox global is "Unknown global". With the defs and a Rojo sourcemap it reports type errors and unknown requires in `--!strict` files (verified). Plain `luau-analyze` (luau 0.742) has no Roblox globals. A Lune 0.10.5 script can open a built place with `@lune/roblox` and assert its tree (verified).
- selene 0.32.0 generates its Roblox std on first run; warnings make it exit non-zero. StyLua 2.6.0 (2026-10-10) `--check` prints a diff and exits 1 on drift.
- rbx_check.py (this skill) passed on the clean fixture with all six checks and failed lint, format and types on a broken copy while build still passed (run 2026-10-10, Windows 11, Python 3.14).
- No MCP server wraps luau-lsp; no Roblox skill set ships a combined check script. TestEZ is archived; Jest Roblox (Roblox/jest-roblox, 3.20.0) is the maintained test framework.
- Practice: reviewers spot AI code by deprecated calls (`wait()`); static checks plus a human playtest are what practitioners name as the bar.

## Open questions

- Does `rojo sourcemap --include-non-scripts` change luau-lsp results enough to make it the default in rbx_check.py?
- Should the types check honour a project `.vscode/settings.json` (`luau-lsp.*` keys) through `--settings`?
- Is there a stable URL for a pinned (versioned) `globalTypes.d.luau` instead of `main`?

## Search plan

Subject:

- `gh release list -R JohnnyMorganz/luau-lsp -L 3`, Kampfkarren/selene, JohnnyMorganz/StyLua, lune-org/lune, luau-lang/luau; luau-lsp README for `analyze` flags
- `https://create.roblox.com/docs/reference/engine/deprecated.md` for new deprecations selene may not know

Tooling:

- `gh search code "luau-lsp analyze" --extension yml` and `gh search code "setup-rokit" --extension yml` (CI practice drift)
- `path:SKILL.md "luau-lsp"` and `path:SKILL.md selene roblox` on GitHub; `https://skills.sh/api/search?q=luau`
- Supersession: `"luau-lsp" deprecated OR replacement <year>`; `CompeyDev/setup-rokit` releases

Practice:

- DevForum `search.json?q=luau-lsp%20ci` and `q=selene%20stylua`; HN Algolia `luau`

Testing:

- Roblox/open-game-eval releases (executable checks on scene state); `gh search code roblox --filename evals.json`; this repository's own `tests/test_scripts.py` (fixture pass and broken-copy fail)

Best sources: the tool repositories' releases and READMEs, real CI workflows found through GitHub code search. Noisy: blog tutorials pinned to old versions.

## Findings log

### R-20261010-3 · 2026-10-10 · Testing: rbx_check.py proven on a fixture and a broken copy
- summary: On a Rojo place fixture, build, sourcemap, lint, format, types and a Lune unit test all passed; adding a file with an unused variable, bad formatting and a `number`/`string` mismatch made lint, format and types fail with build still passing. This is the action evidence the skill demands and the shape of its CI test.
- track: testing
- sources: local run 2026-10-10; tests/test_scripts.py in this repository
- magnitude: n/a (initial)
- applied: C-20261010-1

### R-20261010-2 · 2026-10-10 · Tooling: the CI pipeline real repositories use
- summary: setup-rokit, wally install, rojo sourcemap, curl globalTypes.d.luau, luau-lsp analyze (often with `--ignore="**/_Index/**"`, `--base-luaurc`), selene, stylua --check, rojo build. Response: adopt as references/roblox-ci.yml and as the order of rbx_check.py.
- track: tooling
- sources: https://github.com/rojo-rbx/rojo/tree/master/.github/workflows, https://github.com/CompeyDev/setup-rokit, https://github.com/JohnnyMorganz/luau-lsp
- magnitude: n/a (initial)
- applied: C-20261010-1

### R-20261010-1 · 2026-10-10 · Subject: the type definitions trap and the no-Studio ladder
- summary: luau-lsp needs the Roblox definitions file supplied; luau-analyze lacks Roblox globals; Lune runs pure-Luau tests and reads place files; engine tests need Open Cloud Luau Execution with Jest Roblox.
- track: subject
- sources: https://github.com/JohnnyMorganz/luau-lsp, https://github.com/lune-org/lune, https://github.com/Roblox/jest-roblox
- magnitude: n/a (initial)
- applied: C-20261010-1
