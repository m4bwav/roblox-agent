# AGENTS.md snippet for a Roblox game repository

Copy the section below into the repository's `AGENTS.md` and fill in the angle brackets. Keep the project's own rules; this adds to them.

---

## Roblox rules for agents

- Sync route: <Rojo (`default.project.json`, files are the source of truth) | Studio Script Sync (the place is the source of truth)>. Edit scripts only on disk. Use Studio (MCP or by hand) only for instances, properties, UI and terrain that are not in the files. Never edit one script from both sides.
- Toolchain: versions are pinned in `rokit.toml`. Run tools from the repository root.
- Before saying a change is done, run `python <path to roblox-agent-checks>/scripts/rbx_check.py . --fetch-defs` (or the CI steps in `.github/workflows/`) and fix every failure. A skipped check is reported as skipped, not passed.
- Look up APIs in `https://create.roblox.com/docs/llms.txt` (add `.md` to any docs URL) before using one you are not sure about. Never use `wait`, `spawn`, `delay`, `BodyVelocity` or `Humanoid:LoadAnimation`.
- Security: the server validates every RemoteEvent and RemoteFunction argument (type, range, permission, cooldown). The client never decides currency, damage, inventory or ownership.
- Player data: `UpdateAsync` with `pcall` and retries; session locking through <ProfileStore | the project's lock>; save on `PlayerRemoving` and `BindToClose`.
- Never insert Creator Store models or plugins without checking them for `require(<number>)`, `loadstring`, `getfenv` and HTTP loaders.
- Architecture lives in <docs/architecture.md>. Do not merge or delete code that looks duplicated without checking who calls it. Features stay in one module or folder.
- Never assume: <list the project's traps, for example "StreamingEnabled is on, so parts may not exist on the client">.
- Publishing a place version that players see (`Published`) needs the maintainer's explicit yes every time.
