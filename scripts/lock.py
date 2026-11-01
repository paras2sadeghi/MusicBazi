"""Re-lock dependencies with a minimum release age.

Sets [tool.uv] exclude-newer in pyproject.toml to now minus MIN_AGE_DAYS, then
runs `uv lock`. uv.lock records sha256 hashes for every package.

    uv run scripts/lock.py            # re-lock with the 7-day window
    uv run scripts/lock.py --upgrade  # also move to newest allowed versions

Lowering MIN_AGE_DAYS needs a dated, approved exception in
decisions/0003-lock-policy-uv.md.
"""

import argparse
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

MIN_AGE_DAYS = 7
ROOT = Path(__file__).resolve().parent.parent
PYPROJECT = ROOT / "pyproject.toml"


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--upgrade", action="store_true", help="upgrade within the window")
    args = parser.parse_args()

    cutoff = (datetime.now(timezone.utc) - timedelta(days=MIN_AGE_DAYS)).strftime(
        "%Y-%m-%dT00:00:00Z"
    )
    text = PYPROJECT.read_text(encoding="utf-8")
    new_text, count = re.subn(
        r'^exclude-newer = ".*"$', f'exclude-newer = "{cutoff}"', text, flags=re.M
    )
    if count != 1:
        sys.exit("pyproject.toml: expected exactly one exclude-newer line under [tool.uv]")
    PYPROJECT.write_text(new_text, encoding="utf-8")
    print(f"exclude-newer = {cutoff} ({MIN_AGE_DAYS}-day minimum release age)")

    cmd = ["uv", "lock"] + (["--upgrade"] if args.upgrade else [])
    sys.exit(subprocess.call(cmd, cwd=ROOT))


if __name__ == "__main__":
    main()
