from __future__ import annotations

import subprocess
import sys
from pathlib import Path


COMMANDS = [
    ["scripts/ax_doctor.py"],
    ["scripts/ingest_excel.py", "examples/sample_requirements.csv", "--out", "data/processed/requirements"],
    ["scripts/ingest_figma_export.py", "examples/sample_design_export.json", "--out", "data/processed/ux"],
    ["scripts/parse_uart_log.py", "examples/sample_uart.csv", "--out", "data/processed/uart"],
    ["scripts/build_knowledge_index.py", "data/processed", "--out", "knowledge"],
    ["scripts/make_review_bundle.py", "--out", "knowledge/review_bundle.md"],
]


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    for command in COMMANDS:
        full = [sys.executable, *command]
        print(f"\n> {' '.join(full)}")
        result = subprocess.run(full, cwd=root)
        if result.returncode != 0:
            return result.returncode
    print("\nSmoke test completed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

