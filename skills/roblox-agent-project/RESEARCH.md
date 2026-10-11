# Research: roblox-agent-project

Findings that back [SKILL.md](SKILL.md). Changes they caused are logged in [CHANGELOG.md](CHANGELOG.md); procedural lessons live in [LEARNINGS.md](LEARNINGS.md); test runs in [TESTS.md](TESTS.md); schedule and state in `evergreen.json`. Protocol: MAINTENANCE.md.

Topic: Roblox code on disk for agents (Script Sync versus Rojo, Rokit toolchain, layout, packages). Tier `moderate`. Last refresh 2026-10-10; next due per `evergreen.json`.

## Current understanding

- Studio Script Sync reached full release 2026-06-17 (public beta from 2025-11-12). It syncs Script, LocalScript, ModuleScript and Folder both ways to `.luau` files (`name.luau` ModuleScript, `.server.luau`, `.client.luau`, `.local.luau`, `.legacy.luau`, `.plugin.luau`, `init.*.luau` for scripts with children), up to 10,000 scripts per top-level synced instance and 128 top-level instances, works with Team Create, and resolves conflicts in a Keep Studio / Keep Disk dialog. Non-editable packages do not update from disk. Roblox's coding-harness guide (2026-10-08) still says to enable it under Beta Features, which contradicts the full-release post; treat it as released.
- Roblox says Script Sync is not a Rojo replacement: when the file system is the source of truth, use Rojo. Its external-tools page recommends Rokit, Rojo and Wally.
- Rojo 7.7.1 (2026-10-02) is current; 7.7.0 (2026-07-02) added `rojo syncback` (place to project), websocket transport and `.jsonc`. No 8.x. `rojo init` writes a place template with `.luau` files and runs `git init`.
- Rokit 1.2.0 is the toolchain manager; Aftman is archived. Rokit reads `aftman.toml` and `foreman.toml`. Shims resolve only inside a folder whose manifest lists the tool (verified: outside the project every tool errors "Failed to find tool ... in any project manifest file"). `rokit add` asks for trust on first use; `--force` or `rokit trust` avoid the prompt in a non-interactive shell.
- Packages: Wally 0.3.2 stable, 0.4.0-alpha.0 (2026-09-26) revived it with `--locked`; pesde 0.7.4 (2026-09-09) is the active alternative. luau-lsp 1.70.1 plus the "Luau Language Server Companion" Studio plugin give editor types; Script Sync alone does not.
- Argon 2.0.29 (two-way) and newer tools (Azul, RbxSync, Pesto) exist; none dominates.
- Practice: two writers on one script is the documented risk. No first-hand report of Rojo overwriting MCP edits was found, but the sync tools are built around that conflict.

## Open questions

- Does Script Sync write `.luau` by default for existing `.lua`-named content, and which side wins when Rojo and Script Sync both touch a script? Needs a hands-on test with Studio.
- Wally versus pesde: which will most new projects pick by 2027?
- Does `rokit add` without `--force` hang or fail when no TTY is present? Seen only with `--force` so far.

## Search plan

Subject:

- `https://create.roblox.com/docs/scripting/sync.md`, `https://create.roblox.com/docs/projects/external-tools.md`, `https://create.roblox.com/docs/ai/coding-harness.md`
- `gh release list -R rojo-rbx/rojo -L 3`; `gh release list -R rojo-rbx/rokit -L 3`; DevForum Announcements for Script Sync

Tooling:

- `gh release list` for UpliftGames/wally, pesde-pkg/pesde, argon-rbx/argon, JohnnyMorganz/luau-lsp; `gh repo view <r> --json isArchived,pushedAt`
- `path:SKILL.md "rojo"` and `path:SKILL.md "script sync" roblox` on GitHub; `https://skills.sh/api/search?q=rojo`
- Supersession: `rojo deprecated OR "replaced by" script sync <year>`; aftman, foreman archive flags

Practice:

- DevForum `search.json?q=script%20sync%20rojo` and `q=cursor%20rojo`; r/robloxgamedev RSS `q=rojo`

Testing:

- `rojo build` exit code and `rojo sourcemap` output as the evidence that files map to the place; `InstanceFileSyncService:GetStatus(instance)` for Script Sync (from the coding-harness guide)

Best sources: Roblox docs (`.md`), the rojo-rbx GitHub org, DevForum Announcements. Noisy: listicles comparing sync tools, YouTube setup videos.

## Findings log

### R-20261010-3 · 2026-10-10 · Testing: verified toolchain on Windows 11
- summary: Rokit 1.2.0 from its release zip with `self-install`, then `rokit init` and `rokit add --force` for rojo 7.7.1, StyLua 2.6.0, selene 0.32.0, luau-lsp 1.70.1 and lune 0.10.5; `rojo init`, `rojo build` (0.1 s) and `rojo sourcemap` all exit 0. Tools fail outside a folder with a manifest. Response: adopt (Step 4 notes, roblox-agent-checks runs tools from the project folder).
- track: testing
- sources: local run on the development machine 2026-10-10; https://github.com/rojo-rbx/rokit
- magnitude: n/a (initial)
- applied: C-20261010-1

### R-20261010-2 · 2026-10-10 · Tooling: versions and status of the toolchain
- summary: rojo 7.7.1, rokit 1.2.0, wally 0.3.2 (0.4.0-alpha.0), pesde 0.7.4, argon 2.0.29, luau-lsp 1.70.1; aftman archived; foreman maintained by Roblox but not the community default.
- track: tooling
- sources: https://github.com/rojo-rbx/rojo/releases, https://github.com/rojo-rbx/rokit, https://github.com/UpliftGames/wally/releases, https://github.com/pesde-pkg/pesde/releases
- magnitude: n/a (initial)
- applied: C-20261010-1

### R-20261010-1 · 2026-10-10 · Subject: Script Sync released, coding-harness guide, Rojo stays for file-first
- summary: Script Sync full release 2026-06-17 with the naming table and limits above; Roblox's guide pairs Script Sync with Claude Code and Studio MCP; Roblox says Rojo is the better choice when files are the source of truth.
- track: subject
- sources: https://create.roblox.com/docs/scripting/sync, https://create.roblox.com/docs/ai/coding-harness, https://devforum.roblox.com/t/studio-script-sync-now-in-beta/4065468
- magnitude: n/a (initial)
- applied: C-20261010-1
