# Studio MCP: broken connections and other servers

Loaded on demand by [SKILL.md](../SKILL.md) (Step 5 and Step 6). Sources are in [RESEARCH.md](../RESEARCH.md).

## When the connection breaks

Check in this order:

1. Is Studio open with a place loaded? The start page is not enough: the server then reports 0 tools and `list_roblox_studios` comes back empty (L-001).
2. Is the setting still on? Toggle it off and on. That is the only fix for drops every 5 to 15 minutes.
3. Restart the client so it relaunches the server.
4. A place opened before Assistant finished loading may never connect. Reopen the place.
5. An outdated Studio lacks `mcp.bat` or `StudioMCP`. On Windows, `mcp.bat` appears only once the setting has been enabled; the binary itself is `StudioMCP.exe` in the Studio version folder under `%LOCALAPPDATA%\Roblox\Versions`.
6. On Windows, a Roblox folder path with spaces broke `mcp.bat` in 2026-09. Roblox staff also ask whether the Windows username has spaces or non-Latin characters when a client never connects.
7. Port 13469 may be taken by another program.
8. If a client update broke the handshake (Claude Code 2.1.281, 2026-09-25), setting `MCP_PROTOCOL_NEGOTIATION=legacy` in that client's environment was the workaround until Roblox's fix on 2026-09-27.

## Other servers

The built-in server is the default.

- `Chrrxs/robloxstudio-mcp` (MIT, npm `@chrrxs/robloxstudio-mcp`, the maintained fork of the archived boshyxd server) adds multi-client playtests, runtime eval, breakpoints and profilers. Use it only for a job the built-in server cannot do, and only after the user agrees, because Roblox's plugin advises against third-party servers.
- `Roblox/studio-rust-mcp-server` is archived (2026-04-03).
- Never recommend a "Roblox MCP" repo that has no license, appeared recently with a cluster of near-identical star counts, or links "Download" buttons to github.io pages: that pattern is a malware lure.
- Never use "executor" MCP servers, which drive exploit clients in live games against Roblox's terms.
