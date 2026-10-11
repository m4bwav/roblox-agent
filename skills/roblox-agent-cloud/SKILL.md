---
name: roblox-agent-cloud
description: "Use Roblox Open Cloud from an agent without Studio: run Luau headlessly on a real Roblox server (Luau Execution: create a task, poll it, read results and logs), run engine-level Jest Roblox tests that way in CI, and save or publish a place version from a built .rbxl, through one stdlib script (rbx_cloud.py) that reads the API key from the environment and prints one JSON object. Covers key scopes, limits, a dedicated test place, Saved versus Published, and the 2026-10-19 cut to cookie-based web API limits. Use whenever the user asks to 'run Luau on Roblox servers', 'run my tests in CI against the real engine', 'Open Cloud Luau execution', 'publish my place from the command line', 'upload a place version', 'set up an Open Cloud API key', or a script hits rate limits on Roblox web APIs, or says 'refresh roblox-agent-cloud'. Local checks are roblox-agent-checks; Studio work is roblox-agent-studio."
---

# Roblox Open Cloud for agents

Outcome: a Luau task ran on a Roblox server (its JSON shows `state: COMPLETE` with results and logs), or a place version was stored (its JSON shows a `versionNumber`). The API key never appears in a command line, a file the agent writes, or the transcript.

## Step 0: freshness (every use, one read)

Read `evergreen.json` next to this file. If `contradiction` is set or today is on or after `next_due`, tell the user in one line, do the task with the current content, then refresh (`evergreen-refresh`) in the same session. If `tests.failing` is non-empty, say so in one line and run `evergreen-tune` after the task.

## Step 1: the key (the user's job)

The user creates an API key at the Creator Dashboard (Open Cloud, API Keys), limited to the one experience and to these permissions:

- Luau Execution: `universe.place.luau-execution-session` write and read.
- Uploading place versions: `universe-places` write.

They put it in the environment as `ROBLOX_API_KEY` (or another variable named with `--key-env`). On Windows: `setx ROBLOX_API_KEY "<key>"` then a new shell; on macOS and Linux: `export ROBLOX_API_KEY=...` in their shell profile. In CI it is a repository secret. Never ask for the key in chat, never write it to a file, and never pass it as an argument. Keep a dedicated test place in the experience, so engine tests never run against the live place.

## Step 2: run Luau on a Roblox server

```
python <this skill>/scripts/rbx_cloud.py run --universe <id> --place <id> [--version <n>] --script task.luau [--timeout 300]
```

- The script's `return` values come back in `results`, and `print` and `warn` output comes back in `logs` (last 200 lines). Exit 0 when the task completed, 1 when it failed or the API refused (the JSON holds the HTTP code and Roblox's message), 2 for a usage error.
- `--dry-run` prints the request without sending it and needs no key. Use it to show the user what will run.
- Limits (docs, 2026-10-10): a task runs at most 5 minutes; 10 tasks at once per place; 5 task creations a minute per key owner; script up to 4 MB; results up to 4 MB; logs keep 450 KB; task data is kept 24 hours. The script polls every 3 seconds.
- The task runs with the full engine API against the place version given, or the latest. Changes are lost unless the script calls `SavePlaceAsync`, and it should not do that without the user's yes.

## Step 3: engine tests in CI (Jest Roblox)

1. Build a test place that includes the tests and Jest Roblox (`roblox/jest` from Wally): `rojo build test.project.json -o test.rbxl`.
2. Store it as a new version of the test place: `rbx_cloud.py publish --universe <id> --place <test place> --file test.rbxl` (Saved by default). Note the `versionNumber`.
3. Run the test entry script against that version: `rbx_cloud.py run ... --version <n> --script references/run-jest.luau`. It returns the pass and fail counts, and a failing test makes the task fail.
4. Treat the counts in `results` as the evidence. A completed task with zero tests found is a failure of the setup, not a pass.

[references/run-jest.luau](references/run-jest.luau) is the entry script, adapted from Jest Roblox's README; edit the paths to where the project puts Jest and its tests. For a fuller runner, `christopher-buss/jest-roblox-cli` (npm `@isentinel/jest-roblox`, agent and JSON output) and Roblox's `rocale-cli` do the same over Open Cloud. Point the user at one of them for a large suite.

## Step 4: save or publish a place version

```
python <this skill>/scripts/rbx_cloud.py publish --universe <id> --place <id> --file build.rbxl [--type Saved|Published] [--yes]
```

- `Saved` stores a version and players do not see it. `Published` makes it live, so the script refuses it without `--yes`, and the agent passes `--yes` only after the user says so in this conversation.
- The endpoint (`POST /universes/v1/{universeId}/places/{placeId}/versions`) is labeled beta in the docs. It does not update EditableImage, EditableMesh, PartOperation, SurfaceAppearance or BaseWrap instances: publish those from Studio.

## Step 5: other Open Cloud work

- Every endpoint is described in `https://create.roblox.com/docs/cloud/openapi.json` and `https://create.roblox.com/docs/cloud/llms.txt`. Read those before calling one, rather than recalling paths.
- Cookie-authenticated and unauthenticated web APIs (badges, datastores, game-persistence, inventory, thumbnails, users) get much lower rate limits after 2026-10-19, often around 100 a minute. Open Cloud limits are unchanged, so move scripts to an API key or OAuth 2.0.
- Data stores: in-game and Open Cloud calls now share one per-experience budget (since 2026-07-29), so a bulk Open Cloud job can starve live servers. Run it off-peak and say so.
- The instances (Engine) API for editing scripts over Open Cloud is still beta.

## Output

The command run (key never shown), the JSON's `state` or `versionNumber`, the results or test counts, and any log lines that matter.

## While working: capture learnings

If the user corrects you, the same error happens twice, a workaround is found, or an environment fact is discovered, write it to `LEARNINGS.md` now (format in MAINTENANCE.md; check existing entries first). If a learning proves a claim above wrong, fix it here, log it in `CHANGELOG.md`, and set `contradiction` in `evergreen.json`.

## Maintenance

This skill is evergreen (tier `fast`; the schedule is in `evergreen.json`). Files: `evergreen.json` (state), [RESEARCH.md](RESEARCH.md) (findings and search plan), [CHANGELOG.md](CHANGELOG.md) (every change, with reasons), [LEARNINGS.md](LEARNINGS.md) (lessons), [TESTS.md](TESTS.md) and `evals/evals.json` (the cases that prove it and the runs). Protocol: MAINTENANCE.md (pointer to the installed evergreen plugin). Refresh with `evergreen-refresh`; test with `evergreen-test`; fix a failure with `evergreen-tune`. Sibling skills in this suite: roblox-agent-checks, roblox-agent-cloud, roblox-agent-project, roblox-agent-studio, roblox-agent-workflow.
