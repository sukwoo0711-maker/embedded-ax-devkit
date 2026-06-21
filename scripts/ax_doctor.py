from __future__ import annotations

import importlib.util
import shutil
import subprocess
import sys
from pathlib import Path


REQUIRED_PACKAGES = [
    "pandas",
    "openpyxl",
    "yaml",
    "fitz",
    "pdfplumber",
    "numpy",
    "matplotlib",
    "ruptures",
    "tsfresh",
    "pyod",
]


def has_module(name: str) -> bool:
    return importlib.util.find_spec(name) is not None


def run_version(cmd: list[str]) -> str:
    try:
        result = subprocess.run(cmd, text=True, capture_output=True, timeout=8)
    except Exception as exc:  # pragma: no cover - diagnostics only
        return f"error: {exc}"
    output = (result.stdout or result.stderr).strip()
    return output.splitlines()[0] if output else "installed"


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    print(f"AX doctor root: {root}")
    print(f"Python: {sys.version.split()[0]}")
    print()

    missing = []
    for package in REQUIRED_PACKAGES:
        ok = has_module(package)
        print(f"[{'OK' if ok else 'MISS'}] python package: {package}")
        if not ok:
            missing.append(package)

    print()
    for exe, cmd in [
        ("git", ["git", "--version"]),
        ("gh", ["gh", "--version"]),
        ("ollama", ["ollama", "--version"]),
        ("nvidia-smi", ["nvidia-smi"]),
    ]:
        path = shutil.which(exe)
        if path:
            print(f"[OK] {exe}: {run_version(cmd)}")
        else:
            print(f"[MISS] executable: {exe}")

    print()
    required_dirs = [
        "data/raw/spec_portal",
        "data/raw/ux",
        "data/raw/requirements",
        "data/raw/defects",
        "data/raw/uart",
        "data/processed",
        "knowledge",
        "logs",
    ]
    for rel in required_dirs:
        path = root / rel
        path.mkdir(parents=True, exist_ok=True)
        print(f"[OK] dir: {rel}")

    if missing:
        print()
        print("Install missing packages with:")
        print("  pip install -r requirements.txt")
        return 1

    print()
    print("AX doctor completed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

