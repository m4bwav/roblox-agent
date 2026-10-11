---
name: roblox-agent-project
description: "Put a Roblox game's code on disk so an AI coding agent can edit it as ordinary files under Git: choose between Studio's Script Sync and Rojo, set up the Rokit toolchain (rojo, StyLua, selene, luau-lsp, lune, wally or pesde) in a rokit.toml, scaffold or convert a project (rojo init, rojo syncback), keep one writer per script so Studio, sync and MCP edits never fight, and get editor types from luau-lsp. Use whenever the user asks to 'set up Rojo', 'use Claude Code on my Roblox game from VS Code', 'sync my scripts to files', 'Script Sync or Rojo', 'start a new Roblox project', 'add rokit', 'install wally packages', 'move my place to Git', or reports sync conflicts or lost edits between Studio and disk, or says 'refresh roblox-agent-project'. Running checks is roblox-agent-checks; connecting to Studio is roblox-agent-studio."
---

# Roblox project on disk

Outcome: the game's scripts live in files the agent can edit and Git can track, with a pinned toolchain, one clear sync direction, and a successful `rojo build` (or a Script Sync status read) as proof the files map to the place.

## Step 0: freshness (every use, one read)

Read `evergreen.json` next to this file. If `contradiction` is set or today is on or after `next_due`, tell the user in one line, do the task with the current content, then refresh (`evergreen-refresh`) in the same session. If `tests.failing` is non-empty, say so in one line and run `evergreen-tune` after the task.

## Step 1: survey before changing anything

Look for `*.project.json`, `rokit.toml` / `aftman.toml` / `foreman.toml`, `wally.toml` / `pesde.toml`, `selene.toml`, `stylua.toml` or `.stylua.toml`, `.luaurc`, and `sourcemap.json`. Note which sync route the project already uses. An existing Rojo project stays Rojo. Never convert a team's project without the user's yes.

## Step 2: choose the route

| Route | Use when | What syncs | Limits |
|---|---|---|---|
| Script Sync (built into Studio, full release 2026-06-17) | The place stays the source of truth, the team builds in Studio, the user wants no extra tools; Roblox's own coding-harness guide pairs it with Claude Code | Script, LocalScript, ModuleScript and Folder, both ways | 10,000 scripts per top-level synced instance, 128 top-level instances; packages not marked editable do not update from disk; conflicts open a Keep Studio / Keep Disk dialog the user must answer |
| Rojo 7.7 (`rojo-rbx/rojo`) | Git is the source of truth, CI builds the place, the project uses Wally or pesde packages, or code must build without Studio | Anything described in `default.project.json` (scripts, models, properties, JSON and other data files) | `rojo serve` plus the Studio plugin syncs disk to Studio; `rojo syncback` (7.7.0) pulls a place file into a project once |

Roblox itself says Script Sync is not a Rojo replacement: when the file system must be the source of truth, use Rojo. Argon (`argon-rbx/argon`, two-way) and other two-way tools exist. Mention them only if the user asks.

Script Sync file names: `name.luau` ModuleScript, `name.server.luau` Script, `name.client.luau` client Script, `name.local.luau` LocalScript, `name/` Folder, `name/init.server.luau` a script with children. Set it up in Studio: select the folders in Explorer, right-click, Sync to..., pick a directory. That is the user's click. Afterwards the agent edits those files.

## Step 3: one writer per script (the rule that prevents lost work)

- With Rojo serving, edit scripts on disk only. Do not change the same scripts through Studio MCP `multi_edit` or by hand in Studio: the next sync overwrites one side.
- With Script Sync, the agent edits files and the user resolves any conflict dialog. Never answer Keep Disk or Keep Studio for them.
- Use Studio MCP (roblox-agent-studio) for what is not on disk: instances, properties, UI, terrain.
- Never run Rojo and Script Sync on the same scripts.

## Step 4: toolchain with Rokit (verified on Windows 11, 2026-10-10)

Install Rokit once per machine, after the user agrees: release zip plus `rokit self-install` (adds `~/.rokit/bin` to the user PATH; open a new shell after), or `curl -sSf https://raw.githubusercontent.com/rojo-rbx/rokit/main/scripts/install.sh | bash` on macOS and Linux. Aftman is archived. Rokit reads old `aftman.toml` and `foreman.toml` files, but new projects write `rokit.toml`.

In the project:

```
rokit init
rokit add rojo-rbx/rojo
rokit add JohnnyMorganz/StyLua
rokit add Kampfkarren/selene
rokit add JohnnyMorganz/luau-lsp
rokit add lune-org/lune          # optional: pure-Luau tests and place-file checks
rokit add UpliftGames/wally      # or pesde-pkg/pesde, only if the project uses packages
```

`rokit add` may ask to trust a tool on first use. From a non-interactive agent shell, run `rokit trust <owner/repo>` after the user agrees, or `rokit add --force`. Rokit's shims only resolve inside a folder whose manifest lists the tool, so run tools from the project root. Commit `rokit.toml`; it pins exact versions.

## Step 5: scaffold or convert

- New place: `rojo init` (place template, `.luau` files, runs `git init`; `--skip-git` to skip it). It maps `ReplicatedStorage.Shared` to `src/shared`, `ServerScriptService.Server` to `src/server`, and `StarterPlayer.StarterPlayerScripts.Client` to `src/client`. Then add `selene.toml` with `std = "roblox"`.
- Existing place file: `rojo syncback` pulls it into the project layout. Review the diff before committing.
- `.gitignore`: built `*.rbxl` / `*.rbxlx`, `sourcemap.json`, `Packages/`, `ServerPackages/`, `DevPackages/` (Wally), `roblox_packages/` (pesde).
- Packages: `wally install` or `pesde install` after any manifest change. Point luau-lsp at the Wally types with `wally-package-types` when the project uses it.

## Step 6: editor types

`rojo sourcemap -o sourcemap.json` (add `--include-non-scripts` when code references parts or other non-script instances) gives luau-lsp the DataModel paths. For live types of instances that exist only in Studio, the user can install the "Luau Language Server Companion" Studio plugin. Script Sync on its own does not give the editor types.

## Step 7: prove it

Run `rojo build -o build.rbxl` (Rojo) and check the exit code, or have the user confirm the folder shows as synced in Studio (Script Sync). Then hand over to roblox-agent-checks for lint, format and types. Report the build output line, not "it should work".

## Output

The route chosen and why, the toolchain written to `rokit.toml`, the files created or changed, and the build or sync evidence.

## While working: capture learnings

If the user corrects you, the same error happens twice, a workaround is found, or an environment fact is discovered, write it to `LEARNINGS.md` now (format in MAINTENANCE.md; check existing entries first). If a learning proves a claim above wrong, fix it here, log it in `CHANGELOG.md`, and set `contradiction` in `evergreen.json`.

## Maintenance

This skill is evergreen (tier `moderate`; the schedule is in `evergreen.json`). Files: `evergreen.json` (state), [RESEARCH.md](RESEARCH.md) (findings and search plan), [CHANGELOG.md](CHANGELOG.md) (every change, with reasons), [LEARNINGS.md](LEARNINGS.md) (lessons), [TESTS.md](TESTS.md) and `evals/evals.json` (the cases that prove it and the runs). Protocol: MAINTENANCE.md (pointer to the installed evergreen plugin). Refresh with `evergreen-refresh`; test with `evergreen-test`; fix a failure with `evergreen-tune`. Sibling skills in this suite: roblox-agent-checks, roblox-agent-cloud, roblox-agent-project, roblox-agent-studio, roblox-agent-workflow.
