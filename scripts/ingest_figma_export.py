from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


SCREEN_TYPES = {"FRAME", "COMPONENT", "INSTANCE", "SECTION"}


def walk(node: dict[str, Any], path: list[str] | None = None):
    path = path or []
    name = node.get("name", "")
    node_type = node.get("type", "")
    current_path = [*path, name] if name else path
    yield node, current_path
    for child in node.get("children", []) or []:
        yield from walk(child, current_path)


def summarize_node(node: dict[str, Any], path: list[str]) -> dict[str, Any]:
    box = node.get("absoluteBoundingBox") or {}
    return {
        "id": node.get("id"),
        "name": node.get("name"),
        "type": node.get("type"),
        "path": " / ".join(path),
        "x": box.get("x"),
        "y": box.get("y"),
        "width": box.get("width"),
        "height": box.get("height"),
        "text": node.get("characters"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize design export JSON into UX contract candidates.")
    parser.add_argument("input", type=Path)
    parser.add_argument("--out", type=Path, default=Path("data/processed/ux"))
    args = parser.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)
    data = json.loads(args.input.read_text(encoding="utf-8"))
    root = data.get("document", data)

    screens = []
    texts = []
    for node, path in walk(root):
        node_type = node.get("type")
        if node_type in SCREEN_TYPES:
            screens.append(summarize_node(node, path))
        if node_type == "TEXT":
            texts.append(summarize_node(node, path))

    output = {
        "source_file": str(args.input),
        "screens": screens,
        "texts": texts,
    }
    out_path = args.out / f"{args.input.stem}.ux_candidates.json"
    out_path.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {out_path} with {len(screens)} screen candidate(s) and {len(texts)} text node(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

