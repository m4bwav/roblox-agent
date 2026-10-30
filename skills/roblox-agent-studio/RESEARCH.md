# Research: roblox-agent-studio

Findings that back [SKILL.md](SKILL.md). Changes they caused are logged in [CHANGELOG.md](CHANGELOG.md); procedural lessons live in [LEARNINGS.md](LEARNINGS.md); test runs in [TESTS.md](TESTS.md); schedule and state in `evergreen.json`. Protocol: MAINTENANCE.md.

Topic: connecting AI agents to Roblox Studio through its built-in MCP server. Tier `fast`. Last refresh 2026-10-11; next due per `evergreen.json`.

## Current understanding

- Studio has a built-in MCP server (stdio; local port 13469), built into Studio since about 2026-03 and the recommended route. Enable it in Assistant, then `...`, then Settings > MCP Servers (older builds: Manage MCP Servers), "Enable Studio as MCP server". The setting is per Roblox account and has switched off after Studio updates. Studio runs on Windows and macOS only.
- Launch: Windows `%LOCALAPPDATA%\Roblox\mcp.bat`, run from its own folder (Roblox's plugin uses `cmd.exe /c "cd /d %LOCALAPPDATA%\Roblox && .\mcp.bat"`); macOS `/Applications/RobloxStudio.app/Contents/MacOS/StudioMCP` or the same under `~/Applications`. Quick Connect writes entries for Claude Code, Claude Desktop, Codex CLI, Cursor, Gemini CLI, VS Code and Antigravity.
- Roblox published an official agent plugin, Roblox/roblox-studio-agent-plugin (MIT, created 2026-10-07, v0.2.1). It holds no code: it registers the server for macOS and Windows (`plugin:roblox-studio:macos`, `plugin:roblox-studio:windows`; the other OS entry shows as failed), adds one skill `roblox-get-started` (install Studio, enable MCP, handshake, troubleshooting) and ships evals with mocked tool output. It tells agents not to add a second Studio server or use third-party servers. Claude Code install: `/plugin`, search "Roblox Studio" (the repository has no Claude marketplace file; the directory listing is not yet verified). Codex: `codex plugin marketplace add Roblox/roblox-studio-agent-plugin`.
- Tools (docs updated 2026-10-08; Roblox's plugin README lists a few more, `generate_texture` and `segment_mesh`): script_read, multi_edit, script_search (top 10), script_grep (top 50), search_game_tree, inspect_instance, execute_luau (Edit, Client or Server), get_studio_state, start_stop_play, get_console_output, screen_capture, character_navigation, user_keyboard_input, user_mouse_input, subagent (explore, playtest), generate_mesh, generate_material, generate_procedural_model, wait_job_finished, search_asset, insert_asset, upload_image, store_image, http_get (Roblox docs only), skill, list_roblox_studios. The set varies by Studio version and flags. Every call takes `studio_id` (since 2026-08-19).
- The `skill` tool serves seven Roblox-authored Assistant skills: rbx-create-skill, rbx-debug, rbx-device-simulator-lua, rbx-docs-search, rbx-perf-profiling, rbx-scene-analysis, rbx-unit-test. Creator-authored skills (markdown, name and description frontmatter) shipped 2026-07-09.
- Known problems (DevForum, 2026-06 to 10): drops every 5 to 15 minutes (toggle the setting), the setting switching off after updates, a place opened before Assistant loads never connecting, clients that send before `initialize` dropped, `mcp.bat` breaking on Windows paths with spaces, Claude Code 2.1.281 breaking the handshake (workaround `MCP_PROTOCOL_NEGOTIATION=legacy`, Roblox fix 2026-09-27), stale `script_read`/`script_grep` corrupting line-anchored `multi_edit`, aligned whitespace failing `multi_edit`, no batch undo, edit tools failing during playtests, the playtest subagent reporting false passes.
- `execute_luau` capability sandbox: a server-side, flag-gated restriction (missing LoadUnownedAsset, ScriptGlobals, DataStore, Network: no require of unsandboxed modules, `_G` nil, creating or reparenting scripts fails). It hit users on 2026-09-14 (0.738, fixed 09-18) and about 2026-10-01 (0.741, staff: "we are rolling this back", 2026-10-02). Off on 0.742 in all three data models (R-20261011-2). Users read it as the agent refusing. A third rollout is possible; no opt-out has been announced.
- Practice: experienced users keep code on disk and use MCP to inspect, read logs and playtest; some never playtest through MCP because it is slow. Human playtest stays the final check.
- Community servers: Chrrxs/robloxstudio-mcp (MIT, v3.2.0 on 2026-10-08, about 4,600 npm downloads a week, the maintained fork of boshyxd's archived server) is the most used. WEPPY (`@weppy/roblox-mcp`, AGPL, product) is second. Roblox/studio-rust-mcp-server was archived 2026-04-03. Searches surface lookalike lure repos (68 to 71 stars, no license, September 2026, github.io download buttons) and executor MCPs for exploit clients; never recommend either.

## Open questions

- Is roblox-studio-agent-plugin listed in Anthropic's plugin directory so `/plugin` finds it? Not in claude-plugins-official on 2026-10-11; check again after 2026-10-17.
- Does the `execute_luau` sandbox apply to external MCP clients as well as Assistant? Both were reported affected; staff did not say. Will a third rollout come with a permission prompt for MCP clients?
- Can Chrrxs's server and the built-in one run side by side without tool-name clashes?
- Will Roblox expose Script Analysis (type errors) through MCP? Staff asked for use cases on 2026-05-28.
- Tested here on Windows, Studio 0.742: stdio probe (R-20261011-1) and native tools in a Claude Code session (R-20261011-2), including `multi_edit` and playtests. macOS is untested.

## Search plan

Four tracks; every refresh runs at least one query on each (scope each to the period since the last refresh; add the year).

Subject:

- `https://create.roblox.com/docs/studio/mcp.md` (tool list, setup, Quick Connect clients) and `https://create.roblox.com/docs/ai/coding-harness.md`
- DevForum Announcements JSON `https://devforum.roblox.com/c/updates/announcements/36.json`, filter MCP, Assistant, Studio release notes; `https://devforum.roblox.com/search.json?q=mcp%20after:<date>%20order:latest` and `q=LoadUnownedAsset%20order:latest` (sandbox regressions); fetch `/t/<id>.json` to see staff flair and accepted answers. Release-notes pages on create.roblox.com render empty to WebFetch; use the DevForum "Release Notes for N" threads.

Tooling:

- `gh api repos/Roblox/roblox-studio-agent-plugin` (releases, commits, `skills/`, `evals/`); `gh api repos/Chrrxs/robloxstudio-mcp/releases`; `https://api.npmjs.org/downloads/point/last-week/@chrrxs/robloxstudio-mcp`
- `https://registry.modelcontextprotocol.io/v0/servers?search=roblox`; `gh search repos "roblox mcp" --sort stars` (filter lures: license, created date, star clustering); raw `marketplace.json` of anthropics/claude-plugins-official and claude-plugins-community, grep roblox
- `https://skills.sh/api/search?q=roblox%20studio` and `path:SKILL.md "list_roblox_studios"` on GitHub
- Supersession: `"roblox studio mcp" deprecated OR archived <year>`; archive flag on every server named above

Practice:

- DevForum `search.json?q=claude%20code`, `q=codex%20studio`, topic 4684713 ("What's your setup to use Claude Code?") for new replies
- `https://www.reddit.com/r/robloxgamedev/search.rss?q=mcp&restrict_sr=1&sort=new` (one request per 30 s or more); `hn.algolia.com/api/v1/search_by_date?query=roblox%20mcp`

Testing:

- Roblox's plugin `evals/` folder (mocked tool outputs) for case ideas; `npx @modelcontextprotocol/inspector --cli` against the Studio server when Studio is available
- `Roblox/open-game-eval` `LLM_LEADERBOARD.md` and `EVAL_RELEASE_LOG.md` (agent-on-Studio benchmark, arXiv 2610.02563)

Best sources (primary first): create.roblox.com docs (`.md` form), DevForum Announcements and Studio Bugs threads, the Roblox GitHub org, the npm download API. Noisy: glama and mcpservers listings, vendor blogs (ropilot, creation.dev, obby.fun), "Best Roblox MCP 2026" repos.

## Findings log

Newest first. `Track` is subject, tooling, practice, or testing.

### R-20261030-1 · 2026-10-30 · Subject: Studio MCP token enforcement breaks connections (401)
- track: subject. magnitude: 0.4. applied: C-20261030-1
- From 2026-10-27, StudioMCP helper v1.0.0 enforces `auth.token` (`FFlagStudioMCPProxyTokenEnforce`) and Studio 0.744/0.745 sends no Authorization header on some Windows installs, so `list_roblox_studios` is empty. Staff (shibaxixi) collecting logs; tracked CREATORBUG-30469; no fix as of 2026-10-28. User workaround (flag off) weakens local auth.
- sources: https://devforum.roblox.com/t/4960526

### R-20261030-2 · 2026-10-30 · Quiet elsewhere
- Announcements 10-11..10-29: nothing MCP-specific (Plugin Screenshot Support in Studio 10-27 is a lead for later). No new LoadUnownedAsset sandbox regression. Tooling: Roblox/roblox-studio-agent-plugin one commit (Windows sandbox instructions, 10-15), no release; Chrrxs/robloxstudio-mcp v3.3.0 to v3.4.2 (10-18..10-26), nothing that changes the recommendation. Practice: nothing new. Testing: nothing new.

### R-20261011-3 · 2026-10-11 · Refresh: the execute_luau sandbox was rolled back by staff (settles the contradiction)
- summary: Staff wrote "we are rolling this back" on 2026-10-02 (devforum.roblox.com/t/4908470, accepted answer; also /t/4872488). The same restriction appeared 2026-09-14 on 0.738 behind FFlagStudioAssistantPermissionsScriptCapabilities and was fixed 09-18 (/t/4872775). So it is a flag that has come and gone twice, which is why 0.742 tests saw nothing. Also: Roblox's plugin still not in claude-plugins-official; MCP docs unchanged since 10-08 (27 tools); ChatGPT desktop (former Codex desktop) connection reports, staff checking usernames with spaces or non-Latin characters (/t/4914166). Response: adjust (sandbox rule rewritten, eval case added, contradiction cleared). Magnitude 0.6.

### R-20261011-2 · 2026-10-11 · Testing: native tools in a Claude Code session, multi_edit and the sandbox in all three data models (Studio 0.742.0.7421053)
- summary: A headless `claude -p` session loaded the `mcp__Roblox_Studio__*` tools from the local-scope entry and ran list, create, `script_read`, `multi_edit`, read-back, playtest and cleanup on an unsaved place (T-20261011-2). The 0.741 sandbox did not show in Edit, Server or Client. `execute_luau` returns only its first value; local-scope entries are matched by exact path case. Response: adjust (rule extended to all data models; two working notes).

### R-20261011-1 · 2026-10-11 · Testing: first live connection and playtest on Windows (Studio 0.742.0.7421053)
- summary: With a place open and the setting on, `mcp.bat` existed and the proxy exposed 30 tools; `list_roblox_studios` returns `id` and `name`; the playtest loop ran end to end. The reported 0.741 `execute_luau` sandbox did not show on 0.742 in Edit mode (`_G` a table, a new Script parented to ServerScriptService). Response: adjust (the sandbox becomes a reported failure to recognise, not a rule; the id field named).
- track: testing
- sources: local probe on the development machine 2026-10-11 (T-20261011-1)
- magnitude: 0.3
- applied: C-20261011-1

### R-20261010-6 · 2026-10-10 · Testing: first live probe of the server on Windows (Studio 0.742)
- summary: A stdio probe of `StudioMCP.exe` (in the Studio version folder; no `mcp.bat` until the setting is enabled) got `serverInfo` RobloxStudio 1.0.0 with protocol 2025-06-18 and `tools.listChanged`, but 0 tools and an empty `list_roblox_studios` while Studio sat on its start page with the setting off. So the proxy runs without Studio and only gains tools when a Studio attaches; an empty list is a Studio-side state, not a client problem. Response: adopt (Step 5 order, L-001).
- track: testing
- sources: local probe on the development machine 2026-10-10
- magnitude: 0.2
- applied: C-20261010-2

### R-20261010-5 · 2026-10-10 · Testing: evidence for a Studio connection and Roblox's own evals
- summary: The only proof of a connection is a `list_roblox_studios` result; an empty list means Studio closed, no place open, or the setting off. Roblox's plugin ships evals with mocked tool outputs graded by expectations, and Roblox's OpenGameEval (87 tasks run through Open Cloud in Studio sessions; Claude Fable 5 50.34% pass@1) found that runs which inspect the objects a task touches before editing succeed more often. Response: adopt (Step 2.5 evidence, Step 3 read-before-edit, action case in evals).
- track: testing
- sources: https://github.com/Roblox/roblox-studio-agent-plugin, https://github.com/Roblox/open-game-eval, https://arxiv.org/abs/2610.02563
- magnitude: n/a (initial)
- applied: C-20261010-1

### R-20261010-4 · 2026-10-10 · Practice: pitfalls reported by users
- summary: Stale reads before `multi_edit`, aligned-whitespace failures, no batch undo, edit tools failing during playtest, search caps breaking refactors, the 0.741 `execute_luau` sandbox, Claude Code 2.1.281 handshake break and its legacy-negotiation workaround, Creator Store backdoors widened by agent inserts. Experienced users keep code on disk and use MCP to inspect and playtest.
- track: practice
- sources: https://devforum.roblox.com/t/4684713, https://devforum.roblox.com/t/mcp-keeps-disconnecting-every-5-10-minutes/4717243, https://devforum.roblox.com/t/studio-mcp-turning-off-after-update/4668418, https://devforum.roblox.com/t/studiomcpexe-drops-connection-eof-on-serverdiscover-initialization-request-after-recent-update/4808970
- magnitude: n/a (initial)
- applied: C-20261010-1

### R-20261010-3 · 2026-10-10 · Tooling: community servers, archived servers and lures
- summary: Chrrxs/robloxstudio-mcp is the maintained successor of boshyxd/robloxstudio-mcp (archived 2026-06-06), with tests, CI and about 4,600 npm downloads a week. WEPPY is AGPL and productised. Roblox/studio-rust-mcp-server archived 2026-04-03. No Roblox entry in Anthropic's catalogs; the MCP registry holds one small Studio server. A cluster of lookalike repos and executor MCPs pollutes every search. Response: point (Step 6), warn about lures.
- track: tooling
- sources: https://github.com/Chrrxs/robloxstudio-mcp, https://github.com/boshyxd/robloxstudio-mcp, https://github.com/Roblox/studio-rust-mcp-server, https://registry.modelcontextprotocol.io/v0/servers?search=roblox
- magnitude: n/a (initial)
- applied: C-20261010-1

### R-20261010-2 · 2026-10-10 · Subject: Roblox's official agent plugin (2026-10-07)
- summary: Roblox/roblox-studio-agent-plugin registers Studio's server for both OSes, adds `roblox-get-started`, ships evals, and tells agents to use Studio's `skill` tool for game work and never add a second Studio server. This suite therefore points at it for setup and does not register a server of its own.
- track: subject
- sources: https://github.com/Roblox/roblox-studio-agent-plugin
- magnitude: n/a (initial)
- applied: C-20261010-1

### R-20261010-1 · 2026-10-10 · Subject: built-in Studio MCP server, setup and tools
- summary: Setup path, launch commands per OS, Quick Connect clients, 26 documented tools, `studio_id` on every call, Studio must be open with a place, the `skill` tool's seven Roblox skills, docs page updated 2026-10-08.
- track: subject
- sources: https://create.roblox.com/docs/studio/mcp, https://create.roblox.com/docs/assistant/skills, https://create.roblox.com/docs/ai/coding-harness
- magnitude: n/a (initial)
- applied: C-20261010-1
