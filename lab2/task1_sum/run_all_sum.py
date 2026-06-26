from __future__ import annotations

import subprocess
import sys
from pathlib import Path

SCRIPTS = [
    "sum_threading.py",
    "sum_multiprocessing.py",
    "sum_async.py",
]


def main() -> None:
    current_dir = Path(__file__).parent
    for script in SCRIPTS:
        print("\n" + "=" * 70)
        print(f"Запуск: {script}")
        print("=" * 70)
        subprocess.run([sys.executable, str(current_dir / script)], check=True)


if __name__ == "__main__":
    main()
