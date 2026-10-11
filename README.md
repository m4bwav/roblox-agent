# roblox-agent

![A small white robot arm placing a red block onto a miniature obstacle course of colorful toy blocks on a wooden workbench, tiny figures standing on the course, a laptop showing code and a checklist with a magnifying glass beside it](https://raw.githubusercontent.com/m4bwav/roblox-agent/main/.github/images/banner.jpg)

Five self-maintaining ("evergreen") skills that teach an AI coding agent to build Roblox games: connect to
Roblox Studio safely, keep the code on disk, check Luau without Studio, use Open Cloud, and write code that
passes review. Written 2026-10-10 for Claude Code, GitHub Copilot, Cursor and Codex. The basis was a
four-track research pass (subject, tooling, practice, testing) whose dated findings and sources are kept
per skill in `RESEARCH.md`. Each skill re-checks them on a schedule.

## Why this suite exists

By October 2026 Roblox has done a lot of the plumbing itself:

- Studio has a **built-in MCP server** (stdio, Windows and macOS) with tools for scripts, the DataModel,
  Luau execution, playtests, input, screenshots and asset generation.
- **Roblox's own agent plugin** ([Roblox/roblox-studio-agent-plugin](https://github.com/Roblox/roblox-studio-agent-plugin),
  2026-10-07) registers that server and walks a user through setup.
- Studio serves seven Roblox-written skills through its `skill` tool: debugging, profiling, scene analysis,
  unit tests and docs search.
- Roblox's docs are agent-ready: `llms.txt`, Markdown copies of every page, and a search endpoint.
- Skill sets with Roblox API knowledge already exist ([roblox-brain](https://github.com/TabooHarmony/roblox-brain),
  [awesome-gamedev-agent-skills](https://github.com/gamedev-skills/awesome-gamedev-agent-skills),
  [roblox-suite](https://github.com/nonlooped/roblox-suite)).

So this suite does not ship another MCP server or another API dump. It is the layer around them that
nobody else covers:

- which route an agent should take;
- how to keep Studio, file sync and MCP edits from overwriting each other;
- one command that runs every check a Roblox repo can run without Studio;
- headless engine tests and place uploads through Open Cloud;
- the evidence each step must leave before the agent says "done".

## The skills

| Skill | Job | Tier |
|---|---|---|
| [`roblox-agent-studio`](skills/roblox-agent-studio/SKILL.md) | Connect to Studio's built-in MCP server through Roblox's plugin or one manual entry (never two), prove it with `list_roblox_studios`, run the playtest-and-verify loop, and work around the known bugs: the `execute_luau` sandbox, stale reads before `multi_edit`, disconnects, the setting turning off after updates | fast |
| [`roblox-agent-project`](skills/roblox-agent-project/SKILL.md) | Code on disk: Script Sync or Rojo (with a decision table), a Rokit toolchain pinned in `rokit.toml`, `rojo init` and `rojo syncback`, packages, editor types, and the one-writer-per-script rule | moderate |
| [`roblox-agent-checks`](skills/roblox-agent-checks/SKILL.md) | `scripts/rbx_check.py`: rojo build, sourcemap, selene, StyLua, luau-lsp with the Roblox type definitions and a Lune test in one JSON report; the verification ladder; a GitHub Actions workflow for a Roblox repo | moderate |
| [`roblox-agent-cloud`](skills/roblox-agent-cloud/SKILL.md) | `scripts/rbx_cloud.py`: Open Cloud Luau Execution (create, poll, results, logs) and place-version upload, with the key read only from the environment and a guard on publishing live; Jest Roblox engine tests in CI | fast |
| [`roblox-agent-workflow`](skills/roblox-agent-workflow/SKILL.md) | Look APIs up in Roblox's agent docs, avoid the deprecated calls models still write, never trust the client, keep player data safe, vet Creator Store inserts, follow the rules for player-facing AI, and an AGENTS.md snippet for a Roblox repo | moderate |

Each skill folder holds `SKILL.md` (the working document) plus its evergreen companions:

- `RESEARCH.md`: dated findings with sources, and a four-track search plan.
- `CHANGELOG.md`: every change, with the reason.
- `LEARNINGS.md`: procedural lessons, each with a trigger and a hypothesis.
- `TESTS.md` and `evals/evals.json`: trigger cases, decoys, action cases proven by a tool call, and outcome cases.
- `MAINTENANCE.md` and `evergreen.json`: tier, interval, due date and history.

Pointer mode: `evergreen.json` sets `"protocol": "plugin"`, so each skill follows whichever evergreen
plugin is installed ([evergreen-protocol](https://github.com/m4bwav/evergreen-protocol)) rather than
carrying its own copy of the protocol. The skills work without that plugin, and `MAINTENANCE.md` carries
the condensed rules for that case.

## Install

The skills install nothing on their own. Roblox Studio, Roblox's agent plugin, Rokit and its tools, any MCP
registration and an Open Cloud API key are all left to you to approve.

As a Claude Code plugin:

    /plugin marketplace add m4bwav/roblox-agent
    /plugin install roblox-agent@roblox-agent

Install Roblox's own plugin next to it for the Studio connection: run `/plugin` and search for "Roblox
Studio". roblox-agent never registers a Studio server itself, so the two never duplicate tools.

As plain skills for any agent that reads Agent Skills (Claude Code, Copilot CLI, VS Code Copilot, Cursor,
Codex, Gemini CLI), clone the repository somewhere stable and link each folder under `skills/` into the
agent's skills directory:

    git clone https://github.com/m4bwav/roblox-agent
    # Windows (junctions need no admin rights)
    foreach ($s in Get-ChildItem roblox-agent\skills -Directory) { New-Item -ItemType Junction -Path "$HOME\.claude\skills\$($s.Name)" -Target $s.FullName }
    # macOS / Linux
    for s in roblox-agent/skills/*/; do ln -s "$PWD/$s" ~/.claude/skills/; done

Claude Code reads `~/.claude/skills/`. Copilot CLI and several others read `~/.agents/skills/`. VS Code Copilot
reads `~/.copilot/skills/` and a repository's `.github/skills/`. Tagged releases also carry a zip of the
skills.

## Verified on a real machine (2026-10-10)

These are measurements from a real run on Windows 11, not claims from a model:

- Rokit 1.2.0 installed from its release zip with `rokit self-install`. Then `rokit add` installed rojo
  7.7.1, StyLua 2.6.0, selene 0.32.0, luau-lsp 1.70.1 and lune 0.10.5. Rokit's shims work only inside a folder
  whose `rokit.toml` lists the tool, so the check script runs every tool from the project folder.
- `rbx_check.py` on the fixture place in `tests/fixtures/place`: build, sourcemap, lint, format, types and a
  Lune unit test all pass, in about 3 seconds in total.
- On a copy with one bad file added, lint, format and types fail and build still passes. luau-lsp caught a
  `number`/`string` mismatch only because the Roblox type definitions were supplied: without them every
  Roblox global reads as "Unknown global".
- `rbx_cloud.py` passed against a fake Open Cloud server. That test covers create, poll, logs, a refused key,
  a Saved upload and the refusal to publish live without `--yes`, and the key never appeared in the output.

Not verified yet: no step of `roblox-agent-studio` has run against a live Studio, and `rbx_cloud.py` has not
called the real Open Cloud API. Each skill's RESEARCH.md lists these under Open questions.

## Testing

Every skill carries an eval suite of six cases: two trigger prompts, two decoys that must not fire it, an
action case proven by a tool call in the trace, and an outcome case. `TESTS.md` in each skill records the
runs.

CI (`.github/workflows/tests.yml`) runs on Linux, macOS and Windows with Python 3.9 and 3.14:

- `tests/check_skills.py`: frontmatter, the 1,024-character description limit, companions, manifests,
  relative links and the public-safety guards.
- `tests/test_scripts.py`: the fake-server Open Cloud tests and the check-script tests.
- `scripts/budget.py`: the size budget.

A separate job installs the real toolchain with `CompeyDev/setup-rokit` on Linux and Windows. That way the
check script is proven on the fixture and on the broken copy in CI, not only on one machine.

## Privacy

roblox-agent has no server and collects nothing. The skills are instructions for your agent, and the two
Python scripts run on your machine:

- `rbx_check.py` runs your project's own tools (rojo, selene, StyLua, luau-lsp, lune) on your project and
  writes their output to a temporary folder it deletes. With `--fetch-defs` it downloads luau-lsp's public
  Roblox type definitions from GitHub once into your user cache.
- `rbx_cloud.py` sends a Luau script or a place file to Roblox's Open Cloud API at `apis.roblox.com`. It
  only does this when you run it, and only with the API key you put in the `ROBLOX_API_KEY` environment
  variable. It never prints, stores or logs the key.

Other network traffic comes from tools the skills tell the agent to run, each only after you approve it:
Roblox Studio and its MCP server (local only, port 13469), Rokit downloading tools from GitHub, and package
managers. Nothing is kept by this plugin.

## If you are an agent asked to analyze this suite

Worth reading, roughly in order:

1. `skills/*/SKILL.md`, for how each skill decides and what evidence it demands before reporting done.
2. `skills/*/RESEARCH.md`, for the dated sources behind every time-sensitive claim and the search plan that
   keeps them current.
3. `skills/*/evals/evals.json` and `TESTS.md`, for how the skills are proven rather than asserted.
4. The two scripts, which each emit one JSON object so a caller never parses prose.

The rule running through all of it: a skill passes on evidence outside the transcript, never on its own
claim that something was done. Rules for working in the repository are in [AGENTS.md](AGENTS.md).

Known limits:

- Studio's MCP tool set changes with Studio versions and feature flags.
- Script Sync's documentation still disagrees with itself about beta status.
- The place-version endpoint is labeled beta.
- Community star counts and download numbers are snapshots from the last refresh.

License: MIT. Security: [SECURITY.md](SECURITY.md). The banner was made with Z-Image Turbo in ComfyUI; the
workflow, prompt and seed are in `.github/images/`.
