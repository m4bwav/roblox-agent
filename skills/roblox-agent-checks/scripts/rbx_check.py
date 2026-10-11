"""Run the no-Studio checks on a Rojo-style Roblox project and print one JSON object.

Usage (from anywhere; stdlib only, Python 3.9+):
    python rbx_check.py [project_dir] [--fetch-defs] [--defs PATH] [--lune SCRIPT] [--only a,b] [--skip a,b]

Checks, in order: build (rojo build), sourcemap (rojo sourcemap), lint (selene), format (stylua --check),
types (luau-lsp analyze with the Roblox type definitions), lune (an optional Lune test script).
Each is "pass", "fail" or "skip" (tool missing, nothing to check, or no type definitions) with its exit
code, duration and the last lines of its output. Exit 0 when nothing failed, 1 when a check failed,
2 for a usage error. It never raises: a crash is reported inside the JSON.

Tools run from the project folder, because Rokit's shims only resolve inside a folder whose rokit.toml
(or aftman.toml / foreman.toml) lists the tool. Build output and the sourcemap go to a temporary folder,
so the check writes nothing into the project. --fetch-defs downloads luau-lsp's globalTypes.d.luau
(about 0.9 MB) once into the user cache; without it the types check is skipped with the reason.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.request
from pathlib import Path

DEFS_URL = "https://raw.githubusercontent.com/JohnnyMorganz/luau-lsp/main/scripts/globalTypes.d.luau"
CHECKS = ["build", "sourcemap", "lint", "format", "types", "lune"]
TAIL = 25
TIMEOUT = 600


def cache_dir():
    if os.name == "nt":
        base = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
    else:
        base = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache"))
    return base / "roblox-agent"


def find_tool(name, project):
    """A tool on PATH, or in Rokit's bin folder when the shell that runs us has not picked up PATH yet."""
    found = shutil.which(name)
    if found:
        return found
    rokit_bin = Path.home() / ".rokit" / "bin"
    for cand in (rokit_bin / name, rokit_bin / (name + ".exe")):
        if cand.is_file():
            return str(cand)
    return None


def run(cmd, cwd):
    t0 = time.time()
    try:
        p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=TIMEOUT)
        out = (p.stdout or "") + (p.stderr or "")
        code = p.returncode
    except subprocess.TimeoutExpired:
        out, code = "timed out after %ds" % TIMEOUT, -1
    except OSError as e:
        out, code = str(e), -1
    lines = [l for l in out.splitlines() if l.strip()]
    return {"status": "pass" if code == 0 else "fail", "exit": code, "seconds": round(time.time() - t0, 2),
            "command": " ".join(cmd), "output_tail": lines[-TAIL:], "output_lines": len(lines)}


def skip(reason):
    return {"status": "skip", "reason": reason}


def project_file(project):
    default = project / "default.project.json"
    if default.is_file():
        return default
    others = sorted(project.glob("*.project.json"))
    return others[0] if others else None


def source_paths(pf):
    """Every $path in the project tree that exists and holds Luau, relative to the project folder."""
    try:
        tree = json.loads(pf.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return []
    found = []

    def walk(node):
        if isinstance(node, dict):
            p = node.get("$path")
            if isinstance(p, str):
                found.append(p)
            for k, v in node.items():
                if not k.startswith("$"):
                    walk(v)

    walk(tree.get("tree", {}))
    out = []
    for p in found:
        full = (pf.parent / p)
        if full.is_dir() or full.suffix in (".luau", ".lua"):
            if full.exists() and "_Index" not in full.parts and p not in out:
                out.append(p)
    return out


def get_defs(args_defs, fetch):
    if args_defs:
        p = Path(args_defs).expanduser()
        return (str(p), None) if p.is_file() else (None, "--defs file not found: %s" % p)
    cached = cache_dir() / "globalTypes.d.luau"
    if cached.is_file():
        return str(cached), None
    if not fetch:
        return None, "no Roblox type definitions; rerun with --fetch-defs (downloads %s once)" % DEFS_URL
    try:
        cached.parent.mkdir(parents=True, exist_ok=True)
        with urllib.request.urlopen(DEFS_URL, timeout=60) as r:
            data = r.read()
        cached.write_bytes(data)
        return str(cached), None
    except OSError as e:
        return None, "could not download the type definitions: %s" % e


def parse_args(argv):
    a = {"project": ".", "fetch": False, "defs": None, "lune": None, "only": None, "skip": set()}
    it = iter(argv)
    for x in it:
        if x == "--fetch-defs":
            a["fetch"] = True
        elif x in ("--defs", "--lune", "--only", "--skip"):
            v = next(it, None)
            if v is None:
                raise ValueError("%s needs a value" % x)
            if x == "--only":
                a["only"] = set(v.split(","))
            elif x == "--skip":
                a["skip"] = set(v.split(","))
            else:
                a[x[2:]] = v
        elif x in ("-h", "--help"):
            raise ValueError("help")
        elif x.startswith("--"):
            raise ValueError("unknown option %s" % x)
        else:
            a["project"] = x
    for name in (a["only"] or set()) | a["skip"]:
        if name not in CHECKS:
            raise ValueError("unknown check %s (known: %s)" % (name, ", ".join(CHECKS)))
    return a


def main(argv):
    try:
        a = parse_args(argv)
    except ValueError as e:
        if str(e) == "help":
            print(__doc__.strip())
            return 0
        print(json.dumps({"ok": False, "error": str(e)}))
        return 2
    if a["defs"] and not Path(a["defs"]).expanduser().is_file():
        # A file the user named that is not there is a mistake to report, not a check to skip.
        print(json.dumps({"ok": False, "error": "--defs file not found: %s" % a["defs"]}))
        return 2
    project = Path(a["project"]).resolve()
    report = {"ok": True, "project": project.name, "checks": {}}
    pf = project_file(project) if project.is_dir() else None
    if pf is None:
        report.update(ok=False, error="no *.project.json in %s; not a Rojo-style project" % project)
        print(json.dumps(report, indent=2))
        return 2
    srcs = source_paths(pf)
    toolchain = next((n for n in ("rokit.toml", "aftman.toml", "foreman.toml") if (project / n).is_file()), None)
    report["project_file"] = pf.name
    report["sources"] = srcs
    report["toolchain_file"] = toolchain
    report["packages"] = next((n for n in ("wally.toml", "pesde.toml") if (project / n).is_file()), None)
    if report["packages"] and not any((project / d).is_dir() for d in ("Packages", "roblox_packages")):
        report["warning"] = "packages declared but not installed; run wally install or pesde install first"

    wanted = [c for c in CHECKS if (a["only"] is None or c in a["only"]) and c not in a["skip"]]
    tools = {n: find_tool(n, project) for n in ("rojo", "selene", "stylua", "luau-lsp", "lune")}
    report["tools"] = {k: bool(v) for k, v in tools.items()}
    tmp = Path(tempfile.mkdtemp(prefix="rbx-check-"))
    sourcemap = tmp / "sourcemap.json"
    try:
        for c in wanted:
            if c == "build":
                r = run([tools["rojo"], "build", pf.name, "-o", str(tmp / "check.rbxl")], project) if tools["rojo"] else skip("rojo not found")
            elif c == "sourcemap":
                r = run([tools["rojo"], "sourcemap", pf.name, "-o", str(sourcemap)], project) if tools["rojo"] else skip("rojo not found")
            elif c == "lint":
                if not tools["selene"]:
                    r = skip("selene not found")
                elif not srcs:
                    r = skip("no source paths in the project file")
                else:
                    r = run([tools["selene"]] + srcs, project)
            elif c == "format":
                if not tools["stylua"]:
                    r = skip("stylua not found")
                elif not srcs:
                    r = skip("no source paths in the project file")
                else:
                    r = run([tools["stylua"], "--check"] + srcs, project)
            elif c == "types":
                defs, why = get_defs(a["defs"], a["fetch"])
                if not tools["luau-lsp"]:
                    r = skip("luau-lsp not found")
                elif not srcs:
                    r = skip("no source paths in the project file")
                elif not defs:
                    r = skip(why)
                else:
                    if not sourcemap.is_file() and tools["rojo"]:
                        run([tools["rojo"], "sourcemap", pf.name, "-o", str(sourcemap)], project)
                    cmd = [tools["luau-lsp"], "analyze", "--platform=roblox", "--defs=" + defs,
                           "--ignore=**/_Index/**"]
                    if sourcemap.is_file():
                        cmd.append("--sourcemap=" + str(sourcemap))
                    if (project / ".luaurc").is_file():
                        cmd.append("--base-luaurc=.luaurc")
                    r = run(cmd + srcs, project)
            else:  # lune
                if not a["lune"]:
                    r = skip("no --lune script given")
                elif not tools["lune"]:
                    r = skip("lune not found")
                else:
                    r = run([tools["lune"], "run", a["lune"]], project)
            report["checks"][c] = r
            if r["status"] == "fail":
                report["ok"] = False
    except Exception as e:  # fail soft: the caller always gets JSON
        report.update(ok=False, error="%s: %s" % (type(e).__name__, e))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    report["summary"] = {s: sum(1 for r in report["checks"].values() if r["status"] == s) for s in ("pass", "fail", "skip")}
    print(json.dumps(report, indent=2))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
