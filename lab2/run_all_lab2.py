from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent
SCRIPTS = [
    ROOT / "task1_sum" / "run_all_sum.py",
    ROOT / "task2_parser" / "run_all_parser.py",
]


def main() -> None:
    for script in SCRIPTS:
        print("\n" + "#" * 80)
        print(f"Запуск блока: {script.relative_to(ROOT)}")
        print("#" * 80)
        subprocess.run([sys.executable, str(script)], check=True)


if __name__ == "__main__":
    main()
