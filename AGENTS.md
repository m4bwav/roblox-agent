# Agent rules for roblox-agent

Rules for any AI agent (Claude Code, Copilot, Cursor, Codex, Gemini CLI) working in this repository. `CLAUDE.md` imports this file and `.github/copilot-instructions.md` points here.

Read [README.md](README.md) first. The five skills live under [skills/](skills/). Each is an evergreen unit with its companions beside it: RESEARCH, CHANGELOG, LEARNINGS, TESTS, `evals/evals.json`, MAINTENANCE and `evergreen.json`.

## Rules

- Evergreen units in pointer mode: before editing a skill, read its `evergreen.json`. If `next_due` has passed or `contradiction` is set, say so and refresh after the task (the evergreen plugin's `evergreen-refresh`, otherwise the skill's `MAINTENANCE.md`). Every edit to a SKILL.md gets a CHANGELOG entry with its reason (`R-`, `L-` or `T-` ids, or "user request"). Re-run that skill's `evals/evals.json` (evergreen-test) when the change alters what the skill triggers on, decides or does.
- Research beats recall. Studio MCP tools, Studio settings paths, Open Cloud endpoints, tool versions and Roblox policies move monthly. Never change a command, flag, version, endpoint or tool name from memory: cite the source in RESEARCH.md (an `R-` entry) and log the change in CHANGELOG.md (a `C-` entry).
- `skills/roblox-agent-checks/scripts/rbx_check.py` and `skills/roblox-agent-cloud/scripts/rbx_cloud.py` are stdlib Python 3.9+. Each prints exactly one JSON object and fails soft. `rbx_cloud.py` reads the API key only from the environment and never prints it. Keep both true on Windows, macOS and Linux.
- Skills stay under 200 lines, with a description of at most 1,024 characters (Agent Skills spec) that says what the skill does and names the sibling that owns nearby requests.
- The skills install nothing on their own: Roblox Studio, Roblox's agent plugin, Rokit and its tools, MCP registrations, API keys and community servers are the user's to approve.
- Never name or link the lookalike "Roblox MCP" lure repositories or exploit "executor" servers described in `skills/roblox-agent-studio/RESEARCH.md`, except as a pattern to avoid.
- Before committing, run `python tests/check_skills.py` (structure, companions, manifests, links and the public-safety guards), `python tests/test_scripts.py` and `python scripts/budget.py` from the repository root. CI runs all three, and installs the real toolchain with setup-rokit so the check script is proven on a fixture place.
- Size budget: `scripts/budget.py` sets green, yellow and red limits on what every session loads (descriptions) and on the installed size. Red fails CI. Say so when a change crosses yellow.
- This is a public repository. Nothing in it names a person other than the author credit, a machine, an absolute path on someone's machine, a private project, or a credential. A lesson learned on a particular machine or project is generalised here ("the development machine", "a Roblox place"); the specifics belong in the owner's private notes, never in a commit.
- Versions: when a packaged file changes, bump `.claude-plugin/plugin.json` and tag `vX.Y.Z`. The release workflow checks the tag against the manifest, runs the checks, zips `skills/` and publishes a GitHub release.
- No AI attribution anywhere: no Co-Authored-By trailers and no "generated with" lines in commits, pull requests or files.

## everlast (session knowledge, load on demand)

- `ai-docs/INDEX.md` lists what past sessions learned here. At the start of a task, scan it and open only the entries that match; read `ai-docs/HANDOFF.md` when continuing unfinished work.
- Before finishing a task that hit a dead end, verified a non-obvious command or made a design choice, record it in `ai-docs/` and rewrite `HANDOFF.md` when work is left unfinished. Say "nothing to record" when that is true.
- Anything naming a person, an internal host or name, a credential, or an opinion about people goes to the owner's private notes, never here.
- Link documents with relative markdown links. Every markdown folder has an index that links its files. No wikilinks in the repository.
