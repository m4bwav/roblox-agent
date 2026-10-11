# Decision: build the layer around Roblox's own agent tooling

Date: 2026-10-10. Status: accepted.

## Context

Roblox ships a built-in Studio MCP server, an official agent plugin that registers it (Roblox/roblox-studio-agent-plugin, 2026-10-07), seven skills served through the server's `skill` tool, and agent-ready docs. Community MCP servers (Chrrxs/robloxstudio-mcp) and Roblox API skill sets (roblox-brain, awesome-gamedev-agent-skills, roblox-suite) already exist.

## Decision

roblox-agent ships no MCP server, registers no Studio server, and copies no API reference. It covers what none of those do: route choice, the one-writer-per-script rule between Studio, file sync and MCP, a single no-Studio check command, Open Cloud execution and uploads with key hygiene, review rules for agent-written Roblox code, and the evidence each step must leave.

## Rejected

- Our own MCP server: duplicates the built-in one and the maintained community fork.
- Registering the Studio server in our plugin: duplicate tools next to Roblox's plugin.
- A large Luau API knowledge base: stale fast, and three maintained sets exist to point at.

Related: [../INDEX.md](../INDEX.md)
