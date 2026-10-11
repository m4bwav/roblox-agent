"""Verification program for the roblox-agent wiki (roblox-agent 0.1.1, tag v0.1.1).

Runs every command the wiki shows against a checkout of the release tag, in a fresh demo folder:
    python 2026-10-10-wiki-verify.py <checkout of tag v0.1.1> [<demo folder>]
The demo folder gets copies of the two scripts and of the fixture place, a broken copy of it, a Luau task and
a fake place file. Open Cloud cases run either with --dry-run or against a fake Open Cloud server on 127.0.0.1
(ROBLOX_API_BASE), never against apis.roblox.com. Each case prints "=== label", then "$ command", the merged
stdout and stderr with run-specific values masked (seconds, temporary folders, the cache folder, the port),
then "$ echo $?" and the exit code. The Roblox toolchain (rojo, selene, StyLua, luau-lsp, lune) must be
installed with Rokit for the check cases.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

CHECKOUT = Path(sys.argv[1]).resolve()
DEMO = Path(sys.argv[2] if len(sys.argv) > 2 else Path.home() / "rbx-wiki-demo").resolve()
TASK = "universes/1234567/places/7654321/versions/12/luau-execution-sessions/s1/tasks/t1"

# The commands the pages show, as text. Each runs from the demo folder.
CASES = [
    ("check-help", "python rbx_check.py --help"),
    ("check-fixture", "python rbx_check.py place --fetch-defs --lune tests/greeting.spec.luau"),
    ("check-broken", "python rbx_check.py broken"),
    ("check-only", "python rbx_check.py broken --only types"),
    ("check-no-defs", "python rbx_check.py place --only types --defs missing.d.luau"),
    ("check-not-project", "python rbx_check.py empty"),
    ("check-bad-option", "python rbx_check.py place --only nonsense"),
    ("cloud-help", "python rbx_cloud.py run --help"),
    ("cloud-publish-help", "python rbx_cloud.py publish --help"),
    ("cloud-dry-run", "python rbx_cloud.py run --universe 1234567 --place 7654321 --script task.luau --dry-run"),
    ("cloud-dry-run-version", "python rbx_cloud.py run --universe 1234567 --place 7654321 --version 12 --script task.luau --timeout 120 --dry-run"),
    ("cloud-publish-dry-run", "python rbx_cloud.py publish --universe 1234567 --place 7654321 --file game.rbxl --dry-run"),
    ("cloud-no-key", "python rbx_cloud.py run --universe 1234567 --place 7654321 --script task.luau"),
    ("cloud-run", "python rbx_cloud.py run --universe 1234567 --place 7654321 --version 12 --script task.luau"),
    ("cloud-wrong-key", "python rbx_cloud.py run --universe 1234567 --place 7654321 --script task.luau"),
    ("cloud-publish-saved", "python rbx_cloud.py publish --universe 1234567 --place 7654321 --file game.rbxl"),
    ("cloud-publish-live-refused", "python rbx_cloud.py publish --universe 1234567 --place 7654321 --file game.rbxl --type Published"),
    ("cloud-ids", "python rbx_cloud.py run --universe my-game --place 7654321 --script task.luau"),
]

TASK_LUAU = """-- A Luau Execution task: return values come back as results, prints as logs.
local Players = game:GetService("Players")
print("players online:", #Players:GetPlayers())
return #Players:GetPlayers(), game.PlaceVersion
"""

BAD_LUAU = """--!strict
local unused = 5
local n: number = "oops"
if n == n then print( n ) end
return n
"""


class FakeCloud(BaseHTTPRequestHandler):
    polls = 0

    def log_message(self, *a):
        pass

    def reply(self, code, obj):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        self.rfile.read(int(self.headers.get("Content-Length", 0)))
        if self.headers.get("x-api-key") != "demo-key":
            return self.reply(401, {"code": "UNAUTHENTICATED", "message": "Invalid API key."})
        if self.path.endswith("/luau-execution-session-tasks"):
            return self.reply(200, {"path": TASK, "state": "QUEUED"})
        if "/versions?versionType=" in self.path:
            return self.reply(200, {"versionNumber": 13})
        self.reply(404, {})

    def do_GET(self):
        if self.path == "/cloud/v2/" + TASK:
            FakeCloud.polls += 1
            if FakeCloud.polls < 2:
                return self.reply(200, {"path": TASK, "state": "PROCESSING"})
            return self.reply(200, {"path": TASK, "state": "COMPLETE", "output": {"results": [0, 12]}})
        if self.path == "/cloud/v2/" + TASK + "/logs":
            return self.reply(200, {"luauExecutionSessionTaskLogs": [{"messages": ["players online: 0"]}]})
        self.reply(404, {})


def setup():
    if DEMO.exists():
        shutil.rmtree(DEMO)
    DEMO.mkdir(parents=True)
    shutil.copy(CHECKOUT / "skills/roblox-agent-checks/scripts/rbx_check.py", DEMO)
    shutil.copy(CHECKOUT / "skills/roblox-agent-cloud/scripts/rbx_cloud.py", DEMO)
    shutil.copytree(CHECKOUT / "tests/fixtures/place", DEMO / "place")
    shutil.copytree(CHECKOUT / "tests/fixtures/place", DEMO / "broken")
    (DEMO / "broken/src/shared/Bad.luau").write_text(BAD_LUAU, encoding="utf-8")
    (DEMO / "empty").mkdir()
    (DEMO / "task.luau").write_text(TASK_LUAU, encoding="utf-8")
    (DEMO / "game.rbxl").write_bytes(b"<roblox!" + b"\0" * 64)


def mask(text, port):
    text = re.sub(r'"seconds": [0-9.]+', '"seconds": <s>', text)
    text = re.sub(r"[A-Za-z]:\\[^\"\s]*?rbx-check-[a-z0-9_]+|/tmp/rbx-check-[a-z0-9_]+", "<tmp>", text)
    text = text.replace("\\\\", "\\")
    for cache in (str(Path(os.environ.get("LOCALAPPDATA", "")) / "roblox-agent"), str(Path.home() / ".cache" / "roblox-agent")):
        if cache.strip():
            text = text.replace(cache, "<cache>")
    text = re.sub(re.escape(str(DEMO)), lambda m: "<demo>", text, flags=re.I)
    text = re.sub(re.escape(str(Path.home())), lambda m: "~", text, flags=re.I)
    if port:
        text = text.replace("127.0.0.1:%d" % port, "127.0.0.1:<port>")
    return text


def main():
    setup()
    server = HTTPServer(("127.0.0.1", 0), FakeCloud)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    port = server.server_port
    base = dict(os.environ)
    base.pop("ROBLOX_API_KEY", None)
    base.pop("ROBLOX_API_BASE", None)
    print("=== installed")
    print(subprocess.run([sys.executable, "--version"], capture_output=True, text=True).stdout.strip())
    for tool in ("rojo", "selene", "stylua", "luau-lsp", "lune"):
        r = subprocess.run("%s --version" % tool, shell=True, cwd=DEMO / "place", capture_output=True, text=True)
        print((r.stdout or r.stderr).strip().splitlines()[0] if (r.stdout or r.stderr).strip() else tool + ": not found")
    for label, cmd in CASES:
        env = dict(base)
        if label in ("cloud-run", "cloud-publish-saved", "cloud-publish-live-refused"):
            env.update(ROBLOX_API_BASE="http://127.0.0.1:%d" % port, ROBLOX_API_KEY="demo-key")
        if label == "cloud-wrong-key":
            env.update(ROBLOX_API_BASE="http://127.0.0.1:%d" % port, ROBLOX_API_KEY="revoked-key")
        env["RBX_CLOUD_POLL"] = "0.1"
        run_cmd = cmd.replace("python ", '"%s" ' % sys.executable, 1)
        r = subprocess.run(run_cmd, shell=True, cwd=DEMO, env=env, capture_output=True, text=True,
                           encoding="utf-8", errors="replace")
        print("=== " + label)
        print("$ " + cmd)
        out = mask((r.stdout or "") + (r.stderr or ""), port).rstrip("\n")
        if out:
            print(out)
        print("$ echo $?")
        print(r.returncode)
    server.shutdown()


if __name__ == "__main__":
    main()
