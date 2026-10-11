"""Tests for the two scripts (stdlib unittest). Run from the repository root: python tests/test_scripts.py

rbx_cloud.py is tested against a fake Open Cloud server on 127.0.0.1, so no key or network is needed.
rbx_check.py is tested on tests/fixtures/place: the usage paths always, the real toolchain runs only when
rojo is installed (CI installs it with setup-rokit), otherwise those tests are skipped and say so.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CLOUD = ROOT / "skills" / "roblox-agent-cloud" / "scripts" / "rbx_cloud.py"
CHECK = ROOT / "skills" / "roblox-agent-checks" / "scripts" / "rbx_check.py"
FIXTURE = ROOT / "tests" / "fixtures" / "place"
TASK = "universes/1/places/2/versions/3/luau-execution-sessions/s1/tasks/t1"


def run(script, *args, env=None):
    e = dict(os.environ)
    e.update(env or {})
    p = subprocess.run([sys.executable, str(script)] + list(args), capture_output=True, text=True,
                       encoding="utf-8", env=e, timeout=900)
    try:
        payload = json.loads(p.stdout)
    except ValueError:
        payload = None
    return p.returncode, payload, p.stdout + p.stderr


class FakeCloud(BaseHTTPRequestHandler):
    seen = []
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
        n = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(n)
        FakeCloud.seen.append(("POST", self.path, self.headers.get("x-api-key"), body))
        if self.headers.get("x-api-key") != "test-key":
            return self.reply(401, {"code": "UNAUTHENTICATED"})
        if self.path.endswith("/luau-execution-session-tasks"):
            return self.reply(200, {"path": TASK, "state": "QUEUED"})
        if "/versions?versionType=" in self.path:
            return self.reply(200, {"versionNumber": 7})
        self.reply(404, {})

    def do_GET(self):
        FakeCloud.seen.append(("GET", self.path, self.headers.get("x-api-key"), b""))
        if self.path == "/cloud/v2/" + TASK:
            FakeCloud.polls += 1
            if FakeCloud.polls < 2:
                return self.reply(200, {"path": TASK, "state": "PROCESSING"})
            return self.reply(200, {"path": TASK, "state": "COMPLETE", "output": {"results": [3, "ok"]}})
        if self.path == "/cloud/v2/" + TASK + "/logs":
            return self.reply(200, {"luauExecutionSessionTaskLogs": [{"messages": ["hello from the server"]}]})
        self.reply(404, {})


class CloudTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = HTTPServer(("127.0.0.1", 0), FakeCloud)
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()
        cls.env = {"ROBLOX_API_BASE": "http://127.0.0.1:%d" % cls.server.server_port,
                   "ROBLOX_API_KEY": "test-key", "RBX_CLOUD_POLL": "0.05"}
        cls.tmp = Path(tempfile.mkdtemp())
        (cls.tmp / "task.luau").write_text("return 1 + 2, 'ok'\n", encoding="utf-8")
        (cls.tmp / "game.rbxl").write_bytes(b"<roblox!fake")

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_run_polls_until_complete_and_reads_logs(self):
        code, out, raw = run(CLOUD, "run", "--universe", "1", "--place", "2", "--version", "3",
                             "--script", str(self.tmp / "task.luau"), env=self.env)
        self.assertEqual(code, 0, raw)
        self.assertEqual(out["state"], "COMPLETE")
        self.assertEqual(out["results"], [3, "ok"])
        self.assertEqual(out["logs"], ["hello from the server"])
        self.assertNotIn("test-key", raw, "the key must never be printed")
        post = [s for s in FakeCloud.seen if s[0] == "POST" and s[1].endswith("tasks")][-1]
        self.assertEqual(post[1], "/cloud/v2/universes/1/places/2/versions/3/luau-execution-session-tasks")
        self.assertEqual(json.loads(post[3])["timeout"], "300s")

    def test_wrong_key_is_reported_not_raised(self):
        env = dict(self.env, ROBLOX_API_KEY="bad")
        code, out, raw = run(CLOUD, "run", "--universe", "1", "--place", "2", "--script",
                             str(self.tmp / "task.luau"), env=env)
        self.assertEqual(code, 1, raw)
        self.assertEqual(out["http"], 401)

    def test_publish_saved(self):
        code, out, raw = run(CLOUD, "publish", "--universe", "1", "--place", "2", "--file",
                             str(self.tmp / "game.rbxl"), env=self.env)
        self.assertEqual(code, 0, raw)
        self.assertEqual(out["versionNumber"], 7)
        self.assertIn("versionType=Saved", [s for s in FakeCloud.seen if "versions?" in s[1]][-1][1])

    def test_published_needs_yes(self):
        code, out, _ = run(CLOUD, "publish", "--universe", "1", "--place", "2", "--file",
                           str(self.tmp / "game.rbxl"), "--type", "Published", env=self.env)
        self.assertEqual(code, 2)
        self.assertIn("--yes", out["error"])

    def test_missing_key_and_dry_run(self):
        env = dict(self.env, ROBLOX_API_KEY="")
        code, out, _ = run(CLOUD, "run", "--universe", "1", "--place", "2", "--script",
                           str(self.tmp / "task.luau"), env=env)
        self.assertEqual(code, 2)
        self.assertIn("ROBLOX_API_KEY", out["error"])
        code, out, _ = run(CLOUD, "run", "--universe", "1", "--place", "2", "--script",
                           str(self.tmp / "task.luau"), "--dry-run", env=env)
        self.assertEqual(code, 0)
        self.assertTrue(out["dry_run"])

    def test_subcommand_help_describes_every_option(self):
        for sub, opts in (("run", ["--universe", "--script", "--timeout", "--no-wait", "--dry-run"]),
                          ("publish", ["--file", "--type", "--yes", "--key-env"])):
            p = subprocess.run([sys.executable, str(CLOUD), sub, "--help"], capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(p.returncode, 0)
            lines = p.stdout.splitlines() + [""]
            for opt in opts:
                i = next(n for n, l in enumerate(lines) if l.strip().startswith(opt))
                rest = lines[i].strip()[len(opt):].split()
                # argparse puts the help text on the option's line, or on the next line when the option is long
                nxt = lines[i + 1].strip()
                self.assertTrue(len(rest) > 1 or (nxt and not nxt.startswith("-")), "%s %s has no help" % (sub, opt))

    def test_ids_must_be_numeric(self):
        code, out, _ = run(CLOUD, "run", "--universe", "abc", "--place", "2", "--script", "x", env=self.env)
        self.assertEqual(code, 2)


class CheckTests(unittest.TestCase):
    def test_not_a_project(self):
        with tempfile.TemporaryDirectory() as d:
            code, out, _ = run(CHECK, d)
        self.assertEqual(code, 2)
        self.assertFalse(out["ok"])
        self.assertIn("project.json", out["error"])

    def test_unknown_check_is_a_usage_error(self):
        code, out, _ = run(CHECK, str(FIXTURE), "--only", "nonsense")
        self.assertEqual(code, 2)

    def test_missing_defs_file_is_a_usage_error(self):
        # 0.1.1 skipped the types check and reported ok; a path the user named must exist.
        code, out, _ = run(CHECK, str(FIXTURE), "--defs", "no-such-file.d.luau")
        self.assertEqual(code, 2)
        self.assertFalse(out["ok"])
        self.assertIn("--defs file not found", out["error"])

    def test_reads_the_project_tree(self):
        code, out, raw = run(CHECK, str(FIXTURE), "--only", "lune")
        self.assertEqual(code, 0, raw)
        self.assertEqual(sorted(out["sources"]), ["src/client", "src/server", "src/shared"])
        self.assertEqual(out["toolchain_file"], "rokit.toml")

    @unittest.skipUnless(shutil.which("rojo"), "rojo not installed; CI installs the toolchain with setup-rokit")
    def test_fixture_passes_and_a_broken_copy_fails(self):
        code, out, raw = run(CHECK, str(FIXTURE), "--fetch-defs", "--lune", "tests/greeting.spec.luau")
        self.assertEqual(code, 0, raw)
        self.assertEqual(out["summary"]["fail"], 0, raw)
        self.assertEqual(out["checks"]["types"]["status"], "pass", raw)
        with tempfile.TemporaryDirectory() as d:
            bad = Path(d) / "place"
            shutil.copytree(FIXTURE, bad)
            (bad / "src" / "shared" / "Bad.luau").write_text(
                '--!strict\nlocal n: number = "oops"\nif n == n then print( n ) end\nreturn n\n', encoding="utf-8")
            code, out, raw = run(CHECK, str(bad))
        self.assertEqual(code, 1, raw)
        self.assertEqual(out["checks"]["types"]["status"], "fail", raw)
        self.assertEqual(out["checks"]["format"]["status"], "fail", raw)
        self.assertEqual(out["checks"]["build"]["status"], "pass", raw)


if __name__ == "__main__":
    unittest.main(verbosity=2)
