from __future__ import annotations

from pathlib import Path
import subprocess
import sys


AGENT_ID = "agent.openai.api"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
AGENT_WIKI_ROOT = Path(r"C:\Dropbox\Codex\agent.wiki")


def main(argv: list[str] | None = None) -> int:
    central_helper = AGENT_WIKI_ROOT / "scripts" / "publish_structured_memory_page.py"
    if not central_helper.exists():
        print(f"central structured-memory helper not found: {central_helper}", file=sys.stderr)
        return 2
    command = [
        sys.executable,
        str(central_helper),
        "--profile",
        AGENT_ID,
        "--project-root",
        str(PROJECT_ROOT),
        *(argv if argv is not None else sys.argv[1:]),
    ]
    completed = subprocess.run(command, cwd=str(AGENT_WIKI_ROOT))
    return int(completed.returncode)


if __name__ == "__main__":
    raise SystemExit(main())
