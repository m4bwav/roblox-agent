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
- Library authors have begun shipping AGENTS.md snippets; a DevForum user asked Roblox for AGENTS.md support because rules kept in a script get forgotten.

## Open questions

- Will Roblox remove the old Luau type solver (promised "through 2026"), and what breaks in strict code when it does?
- Will place-scoped Skills or AGENTS.md-style rules reach MCP clients?
- Is the ForceField / Humanoid.Health bypass and similar engine trivia worth a reference file, or better left to the knowledge skill sets?

## Search plan

Subject:

- `https://create.roblox.com/docs/reference/engine/deprecated.md` (diff against the table in Step 2); `https://create.roblox.com/docs/generative-AI.md`
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
