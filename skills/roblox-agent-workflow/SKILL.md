---
name: roblox-agent-workflow
description: "How an AI coding agent designs and writes Roblox games that survive review: plan before code (one-pager, metrics module, enemy cards, fair checkpoints, playtest checklist); look up APIs in Roblox's agent-ready docs (llms.txt, .md pages, deprecated list) instead of recalling them; avoid deprecated calls models still emit (wait, BodyVelocity); never trust the client (RemoteEvent validation, rate limits); keep DataStores safe (UpdateAsync, pcall, session locks); check Creator Store inserts for backdoors; rules for player-facing AI; a repo's AGENTS.md. Use whenever the agent writes or reviews Luau for a Roblox game, or on 'make me an obby', 'design my Roblox game', 'what should playtesters check', 'review my Roblox script', 'is this exploitable', 'save player data', 'add an AI NPC', 'refresh roblox-agent-workflow'. Project setup is roblox-agent-project; running checks is roblox-agent-checks."
---

# Roblox code an agent can stand behind

Outcome: Luau the agent writes or reviews uses current APIs that it looked up and cited, treats every client message as hostile, and keeps player data safe. The reply names each doc page it relied on.

## Step 0: freshness (every use, one read)

Read `evergreen.json` next to this file. If `contradiction` is set or today is on or after `next_due`, tell the user in one line, do the task with the current content, then refresh (`evergreen-refresh`) in the same session. If `tests.failing` is non-empty, say so in one line and run `evergreen-tune` after the task.

## Step 1: design before code (a new game or a gameplay feature)

When the request is a new experience or a gameplay feature (an obby, a round, a map, enemies, a boss, checkpoints), plan it before writing Luau, using [references/game-design.md](references/game-design.md) (after Rogers, *Level Up!*):

- A new experience gets `docs/ONE-PAGER.md` in the repo first (audience and maturity label, core loop as a verb, session length, selling points, comparables, out of scope), shown to the user. Later requests are checked against it.
- Movement numbers live in one metrics ModuleScript, read from the place's `StarterPlayer` and `Workspace` values rather than recalled, and every gap and corridor is built from them.
- Enemies get a card (role, speed, tell, health from hits) before their AI is written; debug commands are owner-only and refused outside Studio.
- The reply ends with what the playtest must check, the agent's own break-it pass and the human checklist (section 7 of the reference).

A bug fix or a code review skips this step.

## Step 2: look it up, do not recall it

Roblox's engine API changes weekly, and Luau ships a release most weeks. Before using an API you are not sure is current, read Roblox's docs:

- `https://create.roblox.com/docs/llms.txt`: the index, with a "For Code Agents" section. Sub-indexes: `/docs/reference/engine/llms.txt` (engine API) and `/docs/cloud/llms.txt` (Open Cloud).
- Add `.md` to any docs URL for Markdown, for example `https://create.roblox.com/docs/reference/engine/classes/DataStoreService.md`.
- Search: `https://create.roblox.com/docs/api/search/<question>` (spaces percent-encoded, no periods) returns JSON matches with Markdown URLs.
- Deprecated APIs: `https://create.roblox.com/docs/reference/engine/deprecated.md`.
- Inside Studio, the MCP `http_get` tool and the `rbx-docs-search` skill reach the same docs (roblox-agent-studio).

Name the page in the reply. If a page cannot be reached, say the API is unverified rather than guessing.

## Step 3: the deprecated calls models still write

| Instead of | Use |
|---|---|
| `wait`, `spawn`, `delay` | `task.wait`, `task.spawn`, `task.delay` |
| `BodyVelocity`, `BodyForce`, `BodyGyro`, `BodyPosition` | `LinearVelocity`, `VectorForce`, `AlignOrientation`, `AlignPosition` |
| `Humanoid:LoadAnimation` | `Humanoid.Animator:LoadAnimation` |
| `PhysicsService` collision groups | the `WorldRoot` collision group APIs (moved 2026-09-03) |
| `Instance.new("Part", parent)` | set properties, then `Parent` last |
| `game.Players` style indexing in shared code | `game:GetService("Players")` |
| legacy chat | `TextChatService` |

A class page marks itself Deprecated but often does not name the replacement; the mover table comes from `https://create.roblox.com/docs/physics/mover-constraints.md`, so cite that page for movers. Check the deprecated list for anything else that looks old. `selene` (roblox-agent-checks) flags some of these.

## Step 4: never trust the client

- Every `RemoteEvent` and `RemoteFunction` handler on the server validates its arguments: the type (`typeof`), the range, and that the player may do it. Check ownership, distance, cooldowns and current state on the server, never a value the client sends.
- Rate-limit remotes per player. Never let the client set currency, damage, position authority or inventory. The client asks; the server decides.
- Do not use `RemoteFunction` server-to-client calls (a client can hang the server). Use `RemoteEvent` pairs instead.
- Server Authority (full release 2026-07-09, opt-in with `Workspace.AuthorityMode = Server`) moves simulation to the server. It forces StreamingEnabled, deferred signals and the Input Action System, and gameplay then uses `BindToSimulation` and `InputAction`. Check the place's setting before writing movement or input code.
- Data from `HttpService` or a module the place does not own is untrusted too.

## Step 5: player data

- Write with `UpdateAsync`, not `SetAsync`, when the value depends on the old one. Wrap every DataStore call in `pcall` and retry with backoff. Save on `PlayerRemoving` and `game:BindToClose`.
- Guard against two servers writing one player's data at once (session locking: ProfileStore or a lock field). Roblox announced built-in session locking and schemas for early 2027; until then the project must do it.
- In-game and Open Cloud DataStore calls share one budget per experience (since 2026-07-29). Do not run bulk jobs at peak.
- `OrderedDataStore` entries cannot be wiped in bulk. Rotate the key (for example per week) for leaderboards that reset.

## Step 6: assets, plugins and backdoors

Before keeping any model, package or plugin from the Creator Store (or one an agent inserted), search it for `require(<number>)`, `loadstring`, `getfenv` and `setfenv`, `HttpService` loaders and obfuscated strings. Studio sandboxes Creator Store inserts by default since 2026-05-13. Do not turn that off to make a model work. Never add an obfuscated plugin.

When a mesh must be made, found, captured or fixed and the polywright plugin is installed, ask polywright through its asset folder ([contract](https://github.com/m4bwav/polywright/blob/main/skills/polywright/references/contract.md)) with the `game-roblox` target, then upload or import the file from `out/` that `manifest.json` names. Limits, styles, scale, collision, performance, avatar items and uploads from the developer's side: [references/3d-models.md](references/3d-models.md).

Pixel-art images in a GUI (`ImageLabel`, `ImageButton`): set `ResampleMode` to `Enum.ResamplerMode.Pixelated`, or Roblox smooths the scaled pixels into blur, and size the element at a whole-number multiple of the image's pixels (R-20261025-1).

## Step 7: AI that players meet

Roblox's generative AI rules (`https://create.roblox.com/docs/generative-AI`) apply to AI inside the game, not to AI used to build it. The creator is responsible for the output. Text shown to players goes through `TextChatService` filtering. Player-facing AI is declared in the Content Maturity questionnaire, and the game shows that it is AI. Long or cross-session AI conversation needs the Restricted (18+) label. In-game APIs: `TextGenerator` (LLM text for NPCs), `GenerationService` (meshes), `AudioTextToSpeech`. Check each page's current limits before relying on them.

## Step 8: the repo's AGENTS.md

When the user wants rules that every agent in the repo follows, adapt [references/AGENTS-snippet.md](references/AGENTS-snippet.md) into their `AGENTS.md` (and a `CLAUDE.md` whose first line is `@AGENTS.md`). Ask first, and keep their existing rules. It records the sync route, the one-writer rule, the checks to run, the security rules above and what the agent must never assume. Keep features in one place, and write down what is called from where, because agents "deduplicating" code have deleted half of a working feature.

## Step 9: deeper knowledge

For depth on one topic, point the user at a maintained skill set instead of improvising: `TabooHarmony/roblox-brain` (29 Roblox skills), `gamedev-skills/awesome-gamedev-agent-skills` (its roblox-luau and roblox-datastores skills are the most installed), or `nonlooped/roblox-suite` (16 skills with evals). They are not part of this plugin. The user decides whether to install one.

## Output

The plan written (Step 1, when it applied), the code or review, the doc pages cited, each security or data rule applied, and the check results from roblox-agent-checks.

## While working: capture learnings

If the user corrects you, the same error happens twice, a workaround is found, or an environment fact is discovered, write it to `LEARNINGS.md` now (format in MAINTENANCE.md; check existing entries first). If a learning proves a claim above wrong, fix it here, log it in `CHANGELOG.md`, and set `contradiction` in `evergreen.json`.

## Maintenance

This skill is evergreen (tier `moderate`; the schedule is in `evergreen.json`). Files: `evergreen.json` (state), [RESEARCH.md](RESEARCH.md) (findings and search plan), [CHANGELOG.md](CHANGELOG.md) (every change, with reasons), [LEARNINGS.md](LEARNINGS.md) (lessons), [TESTS.md](TESTS.md) and `evals/evals.json` (the cases that prove it and the runs). Protocol: MAINTENANCE.md (pointer to the installed evergreen plugin). Refresh with `evergreen-refresh`; test with `evergreen-test`; fix a failure with `evergreen-tune`. Sibling skills in this suite: roblox-agent-checks, roblox-agent-cloud, roblox-agent-project, roblox-agent-studio, roblox-agent-workflow.
