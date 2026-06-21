from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path


DEFAULT_FILES = [
    "templates/ux_contract.yaml",
    "templates/device_contract.yaml",
    "templates/packet_contract.yaml",
    "templates/scheduler_contract.yaml",
    "templates/requirement_trace.yaml",
    "templates/defect_case.yaml",
    "templates/uart_signal_spec.yaml",
]


def append_file(lines: list[str], path: Path) -> None:
    if not path.exists():
        lines.append(f"## Missing: {path}")
        lines.append("")
        return
    lines.append(f"## {path}")
    lines.append("")
    fence = "yaml" if path.suffix.lower() in {".yaml", ".yml"} else "text"
    lines.append(f"```{fence}")
    lines.append(path.read_text(encoding="utf-8", errors="ignore"))
    lines.append("```")
    lines.append("")


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a markdown bundle for Codex/Claude review.")
    parser.add_argument("--out", type=Path, default=Path("knowledge/review_bundle.md"))
    parser.add_argument("--extra", type=Path, nargs="*", default=[])
    args = parser.parse_args()

    root = Path.cwd()
    lines = [
        "# AX Review Bundle",
        "",
        f"Generated: {datetime.now().isoformat(timespec='seconds')}",
        "",
        "Use this bundle to review firmware refactoring against UX, packet, scheduler, requirement, defect, and UART contracts.",
        "",
    ]
    for rel in DEFAULT_FILES:
        append_file(lines, root / rel)
    for extra in args.extra:
        append_file(lines, extra)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

