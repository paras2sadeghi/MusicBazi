"""Health check for the MusicBazi setup.

    uv run --locked scripts/doctor.py
    uv run --locked scripts/doctor.py --offline   # skip the OSV vulnerability query

Checks: lock in sync, pinned server installed, dependency consistency, known
vulnerabilities (OSV; sends only package names and versions), Live bridge,
skill links, agent MCP configs, and stray global AbletonMCP configs.
Exits 1 if any check fails; warnings don't fail.
"""

import argparse
import json
import os
import subprocess
import sys
import tomllib
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SERVER = "mcp-server-ableton-live"
AGENT_CONFIGS = [".mcp.json", ".cursor/mcp.json", ".codex/config.toml"]
GLOBAL_CONFIGS = [
    Path.home() / ".claude.json",
    Path(os.environ.get("APPDATA", "")) / "Claude" / "claude_desktop_config.json",
    Path.home() / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json",
    Path.home() / ".cursor" / "mcp.json",
    Path.home() / ".codex" / "config.toml",
]

results = []


def report(status, name, detail=""):
    results.append(status)
    mark = {"ok": "ok  ", "warn": "warn", "fail": "FAIL"}[status]
    print(f"[{mark}] {name}" + (f" - {detail}" if detail else ""))


def venv_bin(name):
    sub = "Scripts" if os.name == "nt" else "bin"
    suffix = ".exe" if os.name == "nt" else ""
    return ROOT / ".venv" / sub / f"{name}{suffix}"


def sh(cmd):
    return subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)


def pinned_version():
    deps = tomllib.loads((ROOT / "pyproject.toml").read_text("utf-8"))["project"]["dependencies"]
    for dep in deps:
        if dep.startswith(SERVER + "=="):
            return dep.split("==", 1)[1]
    return None


def check_lock():
    r = sh(["uv", "lock", "--check"])
    if r.returncode == 0:
        report("ok", "uv.lock matches pyproject.toml")
    else:
        report("fail", "uv.lock out of date", "run: uv run scripts/lock.py")


def check_server():
    py = venv_bin("python")
    if not py.exists():
        report("fail", ".venv missing", "run: uv run --locked scripts/setup.py")
        return False
    r = sh([py, "-c", f"import importlib.metadata as m; print(m.version('{SERVER}'))"])
    installed, want = r.stdout.strip(), pinned_version()
    if r.returncode == 0 and installed == want:
        report("ok", f"{SERVER} {installed} installed (pinned)")
    else:
        report("fail", f"{SERVER} version", f"installed {installed or 'none'}, pinned {want}")
    r = sh(["uv", "pip", "check", "--python", str(py)])
    if r.returncode == 0:
        report("ok", "dependency tree consistent")
    else:
        report("fail", "dependency tree inconsistent", (r.stdout + r.stderr).strip()[:200])
    return True


def check_osv():
    lock = tomllib.loads((ROOT / "uv.lock").read_text("utf-8"))
    pkgs = [
        (p["name"], p["version"])
        for p in lock.get("package", [])
        if p.get("source", {}).get("registry") and "version" in p
    ]
    body = json.dumps(
        {
            "queries": [
                {"package": {"name": n, "ecosystem": "PyPI"}, "version": v} for n, v in pkgs
            ]
        }
    ).encode()
    req = urllib.request.Request(
        "https://api.osv.dev/v1/querybatch",
        data=body,
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.load(resp)
    except OSError as exc:
        report("warn", "OSV query failed", str(exc))
        return
    hits = [
        f"{n} {v}: {', '.join(x['id'] for x in res.get('vulns', []))}"
        for (n, v), res in zip(pkgs, data.get("results", []))
        if res.get("vulns")
    ]
    if hits:
        report("fail", f"known vulnerabilities in {len(hits)} package(s)", "; ".join(hits))
    else:
        report("ok", f"no known vulnerabilities (OSV, {len(pkgs)} packages)")


def check_bridge():
    r = sh([venv_bin("ableton-live-mcp"), "doctor", "--json"])
    try:
        d = json.loads(r.stdout)
    except ValueError:
        report("fail", "server doctor did not run", (r.stdout + r.stderr).strip()[:200])
        return
    if d.get("script_matches_package"):
        report("ok", "Remote Script installed and matches server", d["script_path"])
    elif d.get("script_installed"):
        report(
            "fail",
            "a different Remote Script is installed",
            "run: uv run --locked scripts/setup.py --install-remote-script --replace",
        )
    else:
        report(
            "fail",
            "Remote Script not installed",
            "run: uv run --locked scripts/setup.py --install-remote-script",
        )
    if d.get("reachable") and d.get("running_script_matches"):
        report("ok", "Live bridge reachable", f"Live {d.get('live_version')}")
    elif d.get("reachable"):
        report(
            "fail",
            "Live is running an old/different bridge",
            f"running {d.get('running_script_version')}; restart Live and reselect AbletonMCP",
        )
    else:
        report(
            "warn",
            "Live bridge not reachable",
            "is Live open with Control Surface = AbletonMCP and no dialog blocking it?",
        )


def check_skills():
    skills = sorted(p.name for p in (ROOT / ".agents" / "skills").iterdir() if p.is_dir())
    missing = [s for s in skills if not (ROOT / ".claude" / "skills" / s / "SKILL.md").exists()]
    if missing:
        report("fail", "Claude skill links missing", ", ".join(missing))
    else:
        report("ok", f"{len(skills)} skills linked for Claude")


def check_agent_configs():
    missing = [c for c in AGENT_CONFIGS if not (ROOT / c).exists()]
    if missing:
        report("warn", "agent MCP configs missing", ", ".join(missing))
    else:
        report("ok", "agent MCP configs present (Claude Code, Cursor, Codex)")


def check_global_configs():
    stray = []
    for path in GLOBAL_CONFIGS:
        try:
            text = path.read_text("utf-8")
        except OSError:
            continue
        if "ableton" in text.lower():
            stray.append(str(path))
    if stray:
        report(
            "warn",
            "global Ableton MCP config found",
            "tools load outside this repo's rules: " + "; ".join(stray),
        )
    else:
        report("ok", "no global Ableton MCP configs")


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--offline", action="store_true", help="skip the OSV query")
    args = parser.parse_args()

    print("MusicBazi doctor\n")
    check_lock()
    if check_server():
        if not args.offline:
            check_osv()
        check_bridge()
    check_skills()
    check_agent_configs()
    check_global_configs()

    fails, warns = results.count("fail"), results.count("warn")
    print(f"\n{len(results) - fails - warns} ok, {warns} warning(s), {fails} failure(s)")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
