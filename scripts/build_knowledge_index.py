from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Iterable


TEXT_SUFFIXES = {".md", ".txt", ".json", ".jsonl", ".yaml", ".yml"}


def iter_text_files(path: Path) -> Iterable[Path]:
    if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES:
        yield path
        return
    for item in sorted(path.rglob("*")):
        if item.suffix.lower() in TEXT_SUFFIXES:
            yield item


def chunk_text(text: str, size: int = 2500, overlap: int = 250) -> Iterable[str]:
    if len(text) <= size:
        yield text
        return
    start = 0
    while start < len(text):
        end = min(start + size, len(text))
        yield text[start:end]
        if end == len(text):
            break
        start = max(0, end - overlap)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a JSONL knowledge index from processed files.")
    parser.add_argument("input", type=Path)
    parser.add_argument("--out", type=Path, default=Path("knowledge"))
    args = parser.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)
    index_path = args.out / "index.jsonl"
    count = 0
    with index_path.open("w", encoding="utf-8") as out:
        for file in iter_text_files(args.input):
            text = file.read_text(encoding="utf-8", errors="ignore")
            for idx, chunk in enumerate(chunk_text(text), start=1):
                digest = hashlib.sha256(f"{file}:{idx}:{chunk[:100]}".encode("utf-8")).hexdigest()[:16]
                out.write(json.dumps({
                    "id": digest,
                    "source_file": str(file),
                    "chunk_index": idx,
                    "text": chunk,
                }, ensure_ascii=False) + "\n")
                count += 1

    print(f"Wrote {count} chunk(s) to {index_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

