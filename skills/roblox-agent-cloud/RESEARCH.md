# Research: roblox-agent-cloud

Findings that back [SKILL.md](SKILL.md). Changes they caused are logged in [CHANGELOG.md](CHANGELOG.md); procedural lessons live in [LEARNINGS.md](LEARNINGS.md); test runs in [TESTS.md](TESTS.md); schedule and state in `evergreen.json`. Protocol: MAINTENANCE.md.

Topic: Roblox Open Cloud for agents (Luau Execution, engine tests, place versions, keys and limits). Tier `fast`. Last refresh 2026-10-10; next due per `evergreen.json`.

## Current understanding

- Luau Execution is labeled STABLE. Create: `POST /cloud/v2/universes/{u}/places/{p}[/versions/{v}]/luau-execution-session-tasks` with `script`, optional `timeout` (default 5 minutes), `binaryInput`, `enableBinaryOutput`. The response's `path` is polled with `GET /cloud/v2/{path}`; `state` is QUEUED, PROCESSING, COMPLETE, FAILED or CANCELLED; `output.results` holds return values; `GET /cloud/v2/{path}/logs` returns `luauExecutionSessionTaskLogs` with `messages` or `structuredMessages`. Limits: 5-minute runtime, 4 MB script and results, 450 KB logs, 10 concurrent tasks per place, 5 creations a minute per key owner, 200 gets a minute, 45 log reads a minute, task data kept 24 hours. Scopes `universe.place.luau-execution-session:write` and `:read`.
- Place versions: `POST /universes/v1/{universeId}/places/{placeId}/versions?versionType=Saved|Published`, `Content-Type: application/octet-stream` (rbxl) or `application/xml` (rbxlx), scope universe-places write, returns `{"versionNumber": n}`. Labeled BETA in the docs on 2026-10-10. Does not update EditableImage, EditableMesh, PartOperation, SurfaceAppearance or BaseWrap.
- Engine tests: Jest Roblox (Roblox/jest-roblox, 3.20.0) runs inside Roblox, including through Luau Execution; runners jest-roblox-cli 0.4.6 (`@isentinel/jest-roblox`, Open Cloud, attached-Studio and headless-Studio backends, agent and JSON output) and Roblox/rocale-cli 0.1.0; GitHub actions thegamerbay/roblox-luau-execution-action and grand-hawk/action-roblox-luau-execution. rbxcloud 0.17.0 (2025-03) is quiet but works.
- 2026 changes: Analytics, Events, Experiments and Thumbnails APIs (2026-08-24), Transaction Refunded webhook (2026-09-23), unified data store budget and 500 MB plus 1 MB per lifetime player storage (2026-07-29); cookie and unauthenticated web API limits for six services drop sharply after 2026-10-19; thumbnails return 200 with an `error` object instead of 503 from 2026-10-26. Machine-readable docs: `/docs/cloud/openapi.json` and `/docs/cloud/llms.txt`.
- rbx_cloud.py (this skill) passed six tests against a fake Open Cloud server, and ran against the real API on 2026-10-11 (R-20261011-1): `output.results` is a JSON array of the return values (tables become objects or arrays), logs come back as `messages`, a script error gives `state: FAILED` with `error.code: SCRIPT_ERROR`, Saved upload returns a `versionNumber`, and Jest Roblox 3.20.1 passed through run-jest.luau once the test place set `LoadStringEnabled`.

## Open questions

- Is the place-version endpoint's BETA label new, and is a v2 replacement coming ("Open Cloud APIs for AI tools", delayed to late 2026; "Unified agentic permission" for Assistant, MCP, plugins and Luau Execution)?
- Does a task-creation limit beyond 5 a minute exist at higher rates (40 in 10 minutes passed on 2026-10-11)?

## Search plan

Subject:

- `https://create.roblox.com/docs/cloud/reference/features/luau-execution.md`, `https://create.roblox.com/docs/cloud/guides/usage-place-publishing.md`, `https://create.roblox.com/docs/cloud/openapi.json` (diff paths and BETA labels)
- DevForum Announcements filtered "Open Cloud" since `last_checked`

Tooling:

- `gh release list` for christopher-buss/jest-roblox-cli, Roblox/rocale-cli, Sleitnick/rbxcloud; Roblox/jest-roblox README version
- `path:SKILL.md "open cloud" roblox` and `path:SKILL.md "luau-execution"` on GitHub; `https://skills.sh/api/search?q=roblox%20open%20cloud`
- Supersession: `"luau execution" roblox deprecated OR v3 <year>`

Practice:

- `gh search code "luau-execution-session-tasks" --extension yml` (CI usage); DevForum `search.json?q=luau%20execution`

Testing:

- this repository's fake-server tests; jest-roblox-cli's agent formatter output as an evidence format; Roblox/open-game-eval's Open Cloud harness

Best sources: Roblox Open Cloud docs (`.md` and openapi.json), DevForum Announcements, the runners' repositories. Noisy: third-party API wrappers' READMEs that lag the docs.

## Findings log

### R-20261011-1 · 2026-10-11 · Live run: Luau Execution, Saved upload and Jest Roblox against a real test place
- Source: live runs with a scoped key on a private test experience (universe and place ids in the private sidecar), rbx_cloud.py from this skill; Wally index for package names.
- Results: `[42, "text", true, {parts, list, version}]` came back as typed JSON; `print` and `warn` lines both in `logs`; engine 0.742. A script `error()` gave `FAILED`, `{code: SCRIPT_ERROR, message: "TaskScript:2: ..."}` and the stack in the logs. Saved uploads returned versions 4 and 5.
- Upload refused with HTTP 409 "Server is busy and unable to process your upload request" twice, 90 seconds apart, while Studio had the place open; accepted at once after Studio closed it.
- Jest Roblox: Wally publishes 3.20.x only as `roblox/jest` and `roblox/jest-globals` (`jsdotlua/jest` stops at 3.10.0). Without `ServerScriptService.LoadStringEnabled` every suite fails with "loadstring() is not available" and Jest reports 0 tests; with it, 2 of 2 passed. run-jest.luau now counts failed suites.
- Rate: 40 task creations at one per 15 seconds, all accepted (44 that day); the DevForum "about 30 an hour" lead did not reproduce.
- Magnitude: m2 (procedure fixes in Step 3 and Step 4; no API change)

### R-20261010-4 · 2026-10-10 · Testing: fake-server tests for rbx_cloud.py
- summary: A local HTTP server reproduces create, poll (PROCESSING then COMPLETE), logs, a 401 for a wrong key and a place upload; the script passes, never prints the key, and refuses Published without `--yes`. Live API run still owed.
- track: testing
- sources: tests/test_scripts.py in this repository
- magnitude: n/a (initial)
- applied: C-20261010-1

### R-20261010-3 · 2026-10-10 · Practice: engine tests in CI go through Luau Execution
- summary: Real repositories that test against the engine build a test place, upload it as a version, and run a Jest entry script through Luau Execution; jest-roblox-cli and rocale-cli wrap this. A dedicated test place and a scoped key are the norm.
- track: practice
- sources: https://github.com/christopher-buss/jest-roblox-cli, https://github.com/Roblox/rocale-cli, https://github.com/Roblox/jest-roblox
- magnitude: n/a (initial)
- applied: C-20261010-1

### R-20261010-2 · 2026-10-10 · Subject: 2026 Open Cloud changes and the 2026-10-19 web API limits
- summary: New analytics and events APIs, the refund webhook, the unified data store budget, and the cut to cookie-based web API limits after 2026-10-19 (Open Cloud unchanged).
- track: subject
- sources: https://devforum.roblox.com/c/updates/announcements/36, https://create.roblox.com/docs/cloud/llms.txt
- magnitude: n/a (initial)
- applied: C-20261010-1

### R-20261010-1 · 2026-10-10 · Subject: Luau Execution and place-version endpoints
- summary: Endpoints, body fields, states, logs shape, limits and scopes as above; place versions endpoint and its instance-type exclusions.
- track: subject
- sources: https://create.roblox.com/docs/cloud/reference/features/luau-execution, https://create.roblox.com/docs/cloud/guides/usage-place-publishing
- magnitude: n/a (initial)
- applied: C-20261010-1
