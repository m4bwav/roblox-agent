---
title: GitHub wiki written and published for 0.1.1
kind: note
date: 2026-10-10
verified: 2026-10-10
stale_after: 2027-04-10
tags: [wiki, docs, 0.1.1, github]
summary: "the wiki's pages, where their git working copy is, how every example was verified against the v0.1.1 tag, the facts found on the way, the gaps in the shipped behaviour, and how to update the wiki; read before touching the wiki"
---

# GitHub wiki for 0.1.1

## Summary

Wrote and published https://github.com/m4bwav/roblox-agent/wiki with the wikiwright skill. It has ten pages plus a sidebar and footer, written from the README, AGENTS.md, the five SKILL.md files and their RESEARCH.md, the two scripts and their `--help`, the tests, the eval runs (TESTS.md) and the live Studio probe. Wiki commit `eb7ce89`. `live`: 10 pages, 0 failures, 4 anchor links, 0 broken. everwrite `tells.py`: 0 strong.

Pages: Home, Getting-Started, Choosing-a-Route, Studio-MCP, Project-on-Disk, Checks, Open-Cloud, Writing-Roblox-Code, FAQ, Development, _Sidebar, _Footer.

## Where the pages are

A sibling of this repository's clone named `roblox-agent.wiki`, branch `master`, remote `https://github.com/m4bwav/roblox-agent.wiki.git`. Plain markdown links, LF line endings.

## How it was published

Preflight: `placeholder` (the maintainer saved the first page). Pages committed over it and pushed with a plain fast-forward.

## How the examples were verified

`2026-10-10-wiki-verify.py` holds every command the pages show as text. It copies the tag's two scripts and fixture place into a fresh demo folder, adds a broken copy, a Luau task and a fake place file, and runs each command there. Open Cloud cases use `--dry-run`, or a fake Open Cloud server on 127.0.0.1 through `ROBLOX_API_BASE`. It masks seconds, temporary folders, the cache folder, the demo folder, the home folder (as `~`) and the port.

- Saved output: `2026-10-10-wiki-verify.out.txt`, 18 cases, run on Windows 11 with Python 3.14.6, rojo 7.7.1, selene 0.32.0, StyLua 2.6.0, luau-lsp 1.70.1 and lune 0.10.5, against `git archive v0.1.1`.
- The Checks and Open-Cloud pages were generated from that output by a fill-in script, so no output was retyped.
- `outputs`: 34 checked, 0 missing, 3 skipped (commands typed into Claude Code, a command list, and the live probe's `initialize` reply, which comes from RESEARCH.md R-20261010-6).
- `snippets`: 0 blocks of a checked language. Two install blocks are skipped (copied from the README; the Windows junction loop is the one used on the development machine). One Rokit command block was counted as commands.
- Repository tests: 10 passed locally. CI passed on all 9 jobs.

Not tested:

- the Claude Code marketplace install;
- Roblox's plugin through `/plugin`;
- the macOS and Linux link commands;
- `roblox-ci.yml` in a game repository;
- `run-jest.luau`;
- any call to the real Open Cloud API;
- a Studio session with a place open.

## Facts verified while writing (not in the README)

- `rbx_check.py` records each tool's full path in `command` (for example `~\.rokit\bin\rojo.EXE` on Windows).
- `output_tail` keeps the last 25 non-empty lines of a tool's output, and `output_lines` counts them all.
- selene's box-drawing characters come out as `\u` escapes in the JSON (it is written with `ensure_ascii`).
- luau-lsp names a failing file twice: once as an absolute path, once as its DataModel path from the sourcemap.
- The Studio MCP server answers `initialize` as "Studio MCP Proxy" (RobloxStudio 1.0.0, protocol 2025-06-18, tools `listChanged`). It lists 0 tools until a Studio attaches.
- `mcp.bat` does not exist before the setting is first enabled; the binary is `StudioMCP.exe` in the Studio version folder.

## Gaps in the shipped behaviour (for 0.1.2)

Gaps 1 and 2 were fixed in 0.1.2 (PR #1) and the wiki was updated for them on 2026-10-11 (see the update below). Gap 3 stands.

1. `rbx_check.py --defs <missing file>` skips the types check and still reports `ok: true` with exit 0 (`check-no-defs` case). A path the user named that does not exist should be a usage error (exit 2). Documented on Checks and FAQ as a "watch for this".
2. `rbx_cloud.py run --help` and `publish --help` list the flags with no descriptions (`cloud-help`, `cloud-publish-help`). The module docstring has them, but argparse shows none.
3. The README's "Verified on a real machine" section still says no step of roblox-agent-studio ran against a live Studio. Since 0.1.1 the server handshake was probed; a session with a place open is still owed.

## Update for 0.1.2 (2026-10-11)

- Ran `2026-10-10-wiki-verify.py` against `git archive v0.1.2`. `diffout` showed one changed area, and only the three expected cases: `check-no-defs` (now `{"ok": false, "error": ...}`, exit 2), `cloud-help` and `cloud-publish-help` (descriptions on every flag). Saved the new output over `2026-10-10-wiki-verify.out.txt`.
- Spliced the three outputs from the saved run into Checks and Open-Cloud by script (no retyping); rewrote the Checks and FAQ sentences about the skip; set 0.1.2 on Home, Development and the footer; Writing-Roblox-Code no longer names a version.
- `check` 0 errors; `outputs` 34 checked, 0 missing, 3 skipped; `snippets` 0 missing; everwrite 0 strong. Wiki commit `230a387`; `live`: 10 pages, 0 failures, 4 anchor links, 0 broken.

## Updating the wiki later

1. `git -C <wiki dir> pull --ff-only`.
2. Extract the new tag (`git archive vX.Y.Z | tar -x -C <scratch>`). Run `python 2026-10-10-wiki-verify.py <scratch> <demo folder>` with the Rokit tools on PATH. Then run `wikiwright.py diffout 2026-10-10-wiki-verify.out.txt <new output>`.
3. Regenerate Checks and Open-Cloud from the new output: copy those two pages back to `.tmpl` with `{{case:<label>}}` placeholders, or edit the changed blocks. Then run `wikiwright.py outputs <wiki dir> <new output> --address ''`, `snippets`, `check --version X.Y.Z` and the everwrite checker.
4. Commit, push, then `wikiwright.py live m4bwav/roblox-agent <wiki dir>`. Pages that name the version:
   - Home ("About these pages");
   - Checks (the 0.1.1 / 0.1.2 `--defs` note);
   - FAQ (the types-skip answer, names 0.1.2);
   - Development (the checkout tag);
   - _Footer.
