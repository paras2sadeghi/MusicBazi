"""Build the locked .venv and link skills. The only supported install path.

    uv run --locked scripts/setup.py
    uv run --locked scripts/setup.py --install-remote-script [--replace]

--install-remote-script copies the server's AbletonMCP Remote Script into
Live's User Library. --replace backs up and replaces a different script that
is already there (e.g. another Ableton MCP). Restart Live afterwards.
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / ".agents" / "skills"
SKILL_LINK_DIRS = [ROOT / ".claude" / "skills"]


def venv_bin(name):
    sub = "Scripts" if os.name == "nt" else "bin"
    suffix = ".exe" if os.name == "nt" else ""
    return ROOT / ".venv" / sub / f"{name}{suffix}"


def run(cmd):
    print("$ " + " ".join(str(c) for c in cmd))
    code = subprocess.call(cmd, cwd=ROOT)
    if code:
        sys.exit(code)


def link_skills():
    for link_dir in SKILL_LINK_DIRS:
        link_dir.mkdir(parents=True, exist_ok=True)
        for skill in sorted(p for p in SKILLS.iterdir() if p.is_dir()):
            link = link_dir / skill.name
            if link.exists():
                continue
            if os.name == "nt":
                # Junctions need no admin rights or Developer Mode.
                subprocess.run(
                    ["cmd", "/c", "mklink", "/J", str(link), str(skill)],
                    check=True,
                    capture_output=True,
                )
            else:
                link.symlink_to(os.path.relpath(skill, link_dir), target_is_directory=True)
            print(f"linked {link.relative_to(ROOT)} -> {skill.relative_to(ROOT)}")
    print("skills linked")


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--install-remote-script", action="store_true")
    parser.add_argument("--replace", action="store_true")
    args = parser.parse_args()

    run(["uv", "sync", "--locked"])
    link_skills()

    if args.install_remote_script:
        cmd = [venv_bin("ableton-live-mcp"), "install"]
        if args.replace:
            cmd.append("--replace")
        run(cmd)

    print("\nDone. Next: uv run --locked scripts/doctor.py")


if __name__ == "__main__":
    main()
