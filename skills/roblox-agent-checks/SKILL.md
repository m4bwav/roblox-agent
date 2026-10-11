---
name: roblox-agent-checks
description: "Verify Roblox Luau code without opening Studio, the way an agent should before saying a change is done: one script (rbx_check.py) runs rojo build, rojo sourcemap, selene, stylua --check, luau-lsp analyze with the Roblox type definitions, and an optional Lune test, and prints one JSON report; plus the verification ladder (static checks, Lune unit tests, place-file assertions with @lune/roblox, engine tests on Roblox servers, a Studio playtest) and a GitHub Actions workflow for a Roblox repo. Use whenever the user asks to 'check my Roblox code', 'lint the Luau', 'type check with luau-lsp', 'does this build', 'set up CI for my Roblox game', 'run the tests', 'why does luau-lsp say Unknown global game', or after the agent edits Luau in a Rojo project, or says 'refresh roblox-agent-checks'. Engine tests through Open Cloud are roblox-agent-cloud; playtests in Studio are roblox-agent-studio."
---

# Roblox checks without Studio

Outcome: a change to Luau code is reported done only with a passing `rbx_check.py` report (or the failing checks named and fixed), and each claim in the reply points at a check that ran.

## Step 0: freshness (every use, one read)

Read `evergreen.json` next to this file. If `contradiction` is set or today is on or after `next_due`, tell the user in one line, do the task with the current content, then refresh (`evergreen-refresh`) in the same session. If `tests.failing` is non-empty, say so in one line and run `evergreen-tune` after the task.

## Step 1: run the checks

The project needs a `*.project.json` (Rojo layout) and the tools in its `rokit.toml` (roblox-agent-project sets that up). From any folder:

```
python <this skill>/scripts/rbx_check.py <project dir> --fetch-defs [--lune tests/run.luau]
```

- Prints one JSON object: `ok`, `sources` (the `$path` folders read from the project file), `tools` found, and per check `status` (pass, fail or skip), `exit`, `seconds`, `command` and `output_tail`. Exit 0 when nothing failed, 1 when a check failed, 2 when the folder is not a Rojo project.
- `--fetch-defs` downloads luau-lsp's `globalTypes.d.luau` (about 0.9 MB) once into the user cache (`%LOCALAPPDATA%\roblox-agent` or `~/.cache/roblox-agent`). Without it the types check is skipped with the reason. Ask before the first download if the user has said network calls need approval. `--defs <file>` uses a copy the project already has.
- `--only types,lint` or `--skip format` narrow the run. Build output and the sourcemap go to a temporary folder, so the check writes nothing into the project.
- It finds tools on PATH or in `~/.rokit/bin`, and runs them from the project folder, because Rokit's shims resolve only where a manifest lists them.

Read the JSON, fix what failed, and run it again until `ok` is true. Quote the summary line (`pass`, `fail`, `skip` counts) in the reply. A skip is not a pass: say which checks were skipped and why.

## Step 2: what each check means

| Check | Tool | Catches | Notes |
|---|---|---|---|
| build | `rojo build` | broken project file, bad `$path`, invalid property values | proves the files map to a place |
| sourcemap | `rojo sourcemap` | the same, plus gives luau-lsp the DataModel paths | add `--include-non-scripts` by hand when code reaches parts by path |
| lint | `selene` with `std = "roblox"` | unused variables, shadowing, deprecated globals, likely bugs | selene builds its Roblox std on first run; warnings exit non-zero |
| format | `stylua --check` | style drift (prints a diff) | fix with `stylua <paths>`, then re-check |
| types | `luau-lsp analyze --platform=roblox --defs=... --sourcemap=...` | type errors, unknown requires, wrong instance paths in `--!strict` files | without the definitions every Roblox global is "Unknown global"; plain `luau-analyze` has no Roblox globals at all |
| lune | `lune run <script>` | logic errors in pure modules | only code that does not touch engine APIs |

## Step 3: the verification ladder

Climb only as far as the change needs, and say which rung was reached:

1. Static: `rbx_check.py` (always, for any Luau change).
2. Pure-Luau unit tests with Lune: keep game logic in modules that take plain values, so Lune can `require` them (`lune run tests/x.spec.luau`).
3. Place-file assertions: a Lune script that opens the built place with `@lune/roblox` (`roblox.deserializePlace(fs.readFile("build.rbxl"))`) and asserts the tree, for example that a ModuleScript exists at the right path. Studio is not needed.
4. Engine tests on Roblox servers through Open Cloud Luau Execution with Jest Roblox (roblox-agent-cloud). They need an API key and a test place.
5. Playtest in Studio over MCP (roblox-agent-studio), and a human playtest for feel. A human playtest is the last word on gameplay, and the reply says when one is still owed.

## Step 4: CI for the user's repository

[references/roblox-ci.yml](references/roblox-ci.yml) is a GitHub Actions workflow: `CompeyDev/setup-rokit` installs the pinned tools, then it downloads the type definitions, runs `wally install` when `wally.toml` exists, and then sourcemap, selene, StyLua, luau-lsp and `rojo build`. Copy it to `.github/workflows/` only when the user asks, and adjust the source folders. A private repository on a paid-minutes plan may prefer a self-hosted runner. Ask before assuming.

## Pitfalls

- A check that passes on the agent's machine but uses an unpinned tool can fail in CI. Versions come from `rokit.toml`, so commit it.
- Wally packages under `Packages/_Index` are skipped by the types check (`--ignore=**/_Index/**`). Run `wally install` first, or every require of a package fails.
- `selene` may flag code the project deliberately allows. Change `selene.toml`, never delete the check.
- luau-lsp prints a harmless warning about `didChangeWatchedFiles`. Ignore it.

## Output

The `rbx_check.py` summary (pass/fail/skip counts), each fix made for a failure, the ladder rung reached, and what is still owed (an engine test or a human playtest).

## While working: capture learnings

If the user corrects you, the same error happens twice, a workaround is found, or an environment fact is discovered, write it to `LEARNINGS.md` now (format in MAINTENANCE.md; check existing entries first). If a learning proves a claim above wrong, fix it here, log it in `CHANGELOG.md`, and set `contradiction` in `evergreen.json`.

## Maintenance

This skill is evergreen (tier `moderate`; the schedule is in `evergreen.json`). Files: `evergreen.json` (state), [RESEARCH.md](RESEARCH.md) (findings and search plan), [CHANGELOG.md](CHANGELOG.md) (every change, with reasons), [LEARNINGS.md](LEARNINGS.md) (lessons), [TESTS.md](TESTS.md) and `evals/evals.json` (the cases that prove it and the runs). Protocol: MAINTENANCE.md (pointer to the installed evergreen plugin). Refresh with `evergreen-refresh`; test with `evergreen-test`; fix a failure with `evergreen-tune`. Sibling skills in this suite: roblox-agent-checks, roblox-agent-cloud, roblox-agent-project, roblox-agent-studio, roblox-agent-workflow.
