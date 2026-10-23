# Research: roblox-agent-workflow

Findings that back [SKILL.md](SKILL.md). Changes they caused are logged in [CHANGELOG.md](CHANGELOG.md); procedural lessons live in [LEARNINGS.md](LEARNINGS.md); test runs in [TESTS.md](TESTS.md); schedule and state in `evergreen.json`. Protocol: MAINTENANCE.md.

Topic: writing reviewable Roblox Luau with agents. Tier `moderate`. Last refresh 2026-10-10; next due per `evergreen.json`.

## Current understanding

- Docs are agent-ready: `create.roblox.com/docs/llms.txt` (2,296 pages, "For Code Agents" section, updated 2026-10-08), engine and Open Cloud sub-indexes, `.md` on any docs URL, `/docs/api/search/<question>` returning JSON, and `/docs/reference/engine/deprecated.md`. `llms-full.txt` exists but is tens of MB; do not load it.
- Deprecated calls practitioners still see from models: `wait`, `spawn`, `delay`, `BodyVelocity` and the other body movers, `Humanoid:LoadAnimation`, PhysicsService collision groups (moved to WorldRoot 2026-09-03). Reviewers have used `wait()` as a tell for AI-written code since 2023.
- The most cited reason experts distrust AI Roblox code is security and data: RemoteEvent exploits, client trust, DataStore corruption, race conditions. Pro-AI writers pre-specify UpdateAsync versus SetAsync and remote patterns because models choose badly. Agents "deduplicating" code have deleted half of a feature.
- Server Authority full release 2026-07-09 (opt-in `Workspace.AuthorityMode = Server`; forces StreamingEnabled, deferred signals, NextGenerationReplication, the Input Action System and fixed simulation; gameplay uses `BindToSimulation` and `InputAction`; 64 attributes per instance). Built-in player data session locking and schemas are on the roadmap for early 2027.
- Creator Store inserts are sandboxed since 2026-05-13 (LoadAsset, loadstring, CapabilityControl, get/setfenv blocked). Free-model backdoors (`require(id)`, HTTP loaders) remain the top Studio risk; obfuscated paid bridge plugins draw suspicion.
- Generative AI policy (`/docs/generative-AI`): creators own third-party AI output; text through TextChatService; declare player-facing AI in the maturity questionnaire; Restricted (18+) for extended or cross-session AI chat; visible AI notices. It targets AI that players meet, not AI used to build. In-game: TextGenerator, GenerationService (Cube 3D), AudioTextToSpeech.
- Knowledge skill sets (tooling track): TabooHarmony/roblox-brain (29 skills, MIT, v2.2 2026-10-02, tests; one scanner warns), gamedev-skills/awesome-gamedev-agent-skills (roblox-luau 3,767 and roblox-datastores 3,480 installs, Apache-2.0), nonlooped/roblox-suite (16 skills, the only one with an eval harness). Pointed at, not copied.
- 3D models (references/3d-models.md, R-20261017-1): 20,000 triangles per mesh (the Importer simplifies above it), watertight, one material per MeshPart, PBR on `SurfaceAppearance` (colour, OpenGL normal, roughness, metalness, emissive mask; not scriptable at run time), textures up to 4096 px but a 1024 px budget per map, 1 stud = 28 cm, at most 4 bone influences; rigid and layered accessories 4,000 triangles; R15 body budgets total 10,742; `CollisionFidelity` Tunable since 2026-09-17; identical MeshContent plus identical appearance instances into one draw call; Open Cloud `assetType` Model takes FBX, glTF, GLB up to 20 MB as packages. Making and fixing meshes is the polywright plugin's job.
- Library authors have begun shipping AGENTS.md snippets; a DevForum user asked Roblox for AGENTS.md support because rules kept in a script get forgotten.
- Game design (references/game-design.md, R-20261023-1): plan before code, after Rogers, *Level Up!*. Engine defaults read 2026-10-23: walk 16, jump height 7.2 or power 50 (UseJumpPower true per the reference), gravity 196.2, respawn 5 s, spawn ForceField 10 s; the place's own values win. Roblox's design pages (design-for-roblox, core-loops, onboarding, prototyping) are the depth to fetch.

## Open questions

- Will Roblox remove the old Luau type solver (promised "through 2026"), and what breaks in strict code when it does?
- Will place-scoped Skills or AGENTS.md-style rules reach MCP clients?
- Is the ForceField / Humanoid.Health bypass and similar engine trivia worth a reference file, or better left to the knowledge skill sets?

## Search plan

Subject:

- `https://create.roblox.com/docs/reference/engine/deprecated.md` (diff against the table in Step 2); `https://create.roblox.com/docs/generative-AI.md`
- 3D models: re-read the pages listed in R-20261017-1 (triangle, texture and accessory limits; importer settings; Open Cloud asset types); DevForum Announcements `q=mesh OR importer OR SurfaceAppearance OR collision`
- DevForum Announcements since `last_checked` for deprecations, Server Authority, data store and security changes; `gh api repos/luau-lang/luau/releases` for language changes

Tooling:

- `gh api repos/TabooHarmony/roblox-brain`, `gamedev-skills/awesome-gamedev-agent-skills`, `nonlooped/roblox-suite` (releases, archive flag, tests); `https://skills.sh/api/search?q=roblox&limit=100` (per-skill installs)
- `path:AGENTS.md roblox rojo` and `path:SKILL.md "RemoteEvent"` on GitHub
- Supersession: `roblox skill archived OR deprecated <year>`

Practice:

- DevForum `search.json?q=ai%20generated%20code`, `q=chatgpt%20deprecated%20wait`, topic 4856246 ("How to Develop with AI the Right Way")
- r/robloxgamedev RSS `q=claude` (posts only; one request per 30 s or more)

Testing:

- `selene` rules that catch deprecated calls; Roblox/open-game-eval tasks touching remotes and data; review cases in this skill's evals (a RemoteEvent handler that trusts the client must be flagged)

Best sources: Roblox docs (`.md`), DevForum Announcements, the three skill sets' repositories. Noisy: AI-written tutorial posts, vendor "best practices" blogs.

## Findings log

### R-20261023-1 · 2026-10-23 · Subject: character defaults and Roblox's own game-design pages
- summary: Read the StarterPlayer, Humanoid, Workspace, Players and SpawnLocation class pages for the values a metrics module starts from: CharacterWalkSpeed 16, CharacterJumpHeight 7.2 studs, CharacterJumpPower 50, CharacterUseJumpPower true (as the reference states it; a place can differ), CharacterMaxSlopeAngle 89, Workspace.Gravity 196.2 studs/s², Players.RespawnTime 5 s, SpawnLocation.Duration 10 s. The units page gives 1 stud = 28 cm and no character size, so the reference measures the character with GetExtentsSize. The docs index lists a "Design your experience" section (design-for-roblox, core-loops, onboarding, prototyping); its onboarding page says new players decide within minutes. Response: adopt (references/game-design.md, Step 1).
- track: subject
- sources: https://create.roblox.com/docs/reference/engine/classes/StarterPlayer.md, https://create.roblox.com/docs/reference/engine/classes/Humanoid.md, https://create.roblox.com/docs/reference/engine/classes/Workspace.md, https://create.roblox.com/docs/reference/engine/classes/Players.md, https://create.roblox.com/docs/reference/engine/classes/SpawnLocation.md, https://create.roblox.com/docs/physics/units.md, https://create.roblox.com/docs/production/game-design/design-for-roblox.md, https://create.roblox.com/docs/production/game-design/core-loops.md, https://create.roblox.com/docs/production/game-design/onboarding.md
- magnitude: minor (new reference and step)
- applied: C-20261023-1

### R-20261017-1 · 2026-10-17 · Subject: 3D models for Roblox (limits, PBR, scale, collision, avatar items, uploads)
- summary: Read the current modelling, texture, importer, units, collision, performance, avatar, UGC validation and Open Cloud asset pages and dated DevForum announcements; written up from the developer's side in references/3d-models.md, with mesh making sent to polywright. The texture page both allows 4096 px uploads and caps UV texture maps at 1024 px; the reference states both. `parts/meshes` says four PBR maps while `surface-appearance` lists five (emissive mask added). Response: adopt (new reference, Step 5 pointer).
- track: subject
- sources: https://create.roblox.com/docs/art/modeling/specifications.md, https://create.roblox.com/docs/art/modeling/texture-specifications.md, https://create.roblox.com/docs/art/modeling/surface-appearance.md, https://create.roblox.com/docs/art/modeling/export-requirements.md, https://create.roblox.com/docs/art/blender.md, https://create.roblox.com/docs/parts/meshes.md, https://create.roblox.com/docs/studio/importer.md, https://create.roblox.com/docs/art/modeling/reimport.md, https://create.roblox.com/docs/physics/units.md, https://create.roblox.com/docs/parts/solid-modeling.md, https://create.roblox.com/docs/performance-optimization/improve.md, https://create.roblox.com/docs/avatar/character-bodies/specifications.md, https://create.roblox.com/docs/avatar/rigid-accessories/specifications.md, https://create.roblox.com/docs/avatar/layered-accessories/specifications.md, https://create.roblox.com/docs/avatar-setup/auto-setup-requirements.md, https://create.roblox.com/docs/marketplace/validation-system.md, https://create.roblox.com/docs/parts/model-generation.md, https://create.roblox.com/docs/cloud/guides/usage-assets.md, https://devforum.roblox.com/t/2057539 (3D Importer full release, 2022-11-17), https://devforum.roblox.com/t/4515374 (solid modelling on meshes beta, 2026-03-12), https://devforum.roblox.com/t/4709282 (UGC validation visualiser beta, 2026-06-29), https://devforum.roblox.com/t/4703282 (64 terrain materials early access, 2026-06-25), https://devforum.roblox.com/t/4859863 (Auto-Reimport beta, 2026-09-08), https://devforum.roblox.com/t/4878198 (Tunable collision, 2026-09-17)
- magnitude: minor (new reference)
- applied: C-20261017-2

### R-20261010-4 · 2026-10-10 · Testing: what a good review looks like
- summary: The evidence for this skill is a review that cites the docs page used and flags client trust and deprecated calls; selene catches part of the deprecated list mechanically. Eval cases use a seeded insecure RemoteEvent handler and a `wait()` call.
- track: testing
- sources: https://create.roblox.com/docs/reference/engine/deprecated, https://github.com/Kampfkarren/selene
- magnitude: n/a (initial)
- applied: C-20261010-1

### R-20261010-3 · 2026-10-10 · Tooling: three skill sets carry Roblox API depth
- summary: roblox-brain, awesome-gamedev-agent-skills and roblox-suite are the serious Roblox knowledge sets; the rest are thin or untested. Response: point (Step 8), do not copy.
- track: tooling
- sources: https://github.com/TabooHarmony/roblox-brain, https://github.com/gamedev-skills/awesome-gamedev-agent-skills, https://github.com/nonlooped/roblox-suite, https://skills.sh/api/search?q=roblox
- magnitude: n/a (initial)
- applied: C-20261010-1

### R-20261010-2 · 2026-10-10 · Practice: where AI Roblox code fails review
- summary: Deprecated APIs, client trust, DataStore misuse, refactor deletions, hallucinated engine facts. Architecture and security stay with the human; documents of what the agent must never assume help.
- track: practice
- sources: https://devforum.roblox.com/t/4684713, https://devforum.roblox.com/t/4856246
- magnitude: n/a (initial)
- applied: C-20261010-1

### R-20261010-1 · 2026-10-10 · Subject: agent-ready docs, Server Authority, sandboxed inserts, AI policy
- summary: llms.txt and `.md` docs with a search endpoint and deprecated list; Server Authority full release and its forced settings; Creator Store sandboxing; the generative AI policy for player-facing AI.
- track: subject
- sources: https://create.roblox.com/docs/llms.txt, https://devforum.roblox.com/c/updates/announcements/36, https://create.roblox.com/docs/generative-AI
- magnitude: n/a (initial)
- applied: C-20261010-1
