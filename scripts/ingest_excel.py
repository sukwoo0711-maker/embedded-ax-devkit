from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable

import pandas as pd


EXCEL_SUFFIXES = {".xls", ".xlsx", ".xlsm", ".xlsb", ".ods", ".odf", ".odt"}


def iter_files(path: Path) -> Iterable[Path]:
    if path.is_file():
        yield path
        return
    for item in sorted(path.rglob("*")):
        if item.suffix.lower() in EXCEL_SUFFIXES or item.suffix.lower() == ".csv":
            yield item


def clean_value(value):
    if pd.isna(value):
        return None
    if hasattr(value, "isoformat"):
        return value.isoformat()
    return value


def ingest_workbook(path: Path, out_dir: Path) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = path.stem
    jsonl_path = out_dir / f"{stem}.jsonl"
    md_path = out_dir / f"{stem}.md"
    records = []

    if path.suffix.lower() == ".csv":
        sheets = {"csv": pd.read_csv(path)}
    else:
        sheets = pd.read_excel(path, sheet_name=None)

    with jsonl_path.open("w", encoding="utf-8") as jf, md_path.open("w", encoding="utf-8") as mf:
        mf.write(f"# {path.name}\n\n")
        for sheet_name, df in sheets.items():
            df = df.dropna(how="all")
            mf.write(f"## Sheet: {sheet_name}\n\n")
            mf.write(f"Rows: {len(df)}\n\n")
            if not df.empty:
                mf.write(df.head(30).to_markdown(index=False))
                mf.write("\n\n")

            for source_row, (_, row) in enumerate(df.iterrows(), start=2):
                payload = {
                    "source_file": str(path),
                    "sheet": str(sheet_name),
                    "row": source_row,
                    "columns": {str(k): clean_value(v) for k, v in row.items()},
                }
                jf.write(json.dumps(payload, ensure_ascii=False) + "\n")
                records.append(payload)

    return {
        "source": str(path),
        "jsonl": str(jsonl_path),
        "markdown": str(md_path),
        "records": len(records),
        "sheets": list(sheets.keys()),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert Excel/CSV requirements to JSONL and Markdown.")
    parser.add_argument("input", type=Path)
    parser.add_argument("--out", type=Path, default=Path("data/processed/requirements"))
    args = parser.parse_args()

    summaries = []
    for file in iter_files(args.input):
        summaries.append(ingest_workbook(file, args.out))

    summary_path = args.out / "ingest_summary.json"
    summary_path.write_text(json.dumps(summaries, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Processed {len(summaries)} workbook(s). Summary: {summary_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
