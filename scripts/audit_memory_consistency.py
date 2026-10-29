from __future__ import annotations

from pathlib import Path
import subprocess
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
AGENT_WIKI_ROOT = Path(r"C:\Dropbox\Codex\agent.wiki")


def main(argv: list[str] | None = None) -> int:
    central_helper = AGENT_WIKI_ROOT / "scripts" / "audit_memory_consistency.py"
    if not central_helper.exists():
        print(f"central memory consistency helper not found: {central_helper}", file=sys.stderr)
        return 2
    command = [
        sys.executable,
        str(central_helper),
        *(argv if argv is not None else sys.argv[1:]),
    ]
    completed = subprocess.run(command, cwd=str(PROJECT_ROOT))
    return int(completed.returncode)


if __name__ == "__main__":
    raise SystemExit(main())
