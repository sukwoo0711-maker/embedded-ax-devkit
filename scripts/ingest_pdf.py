from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable


PDF_SUFFIXES = {".pdf"}


def iter_pdfs(path: Path) -> Iterable[Path]:
    if path.is_file() and path.suffix.lower() in PDF_SUFFIXES:
        yield path
        return
    for item in sorted(path.rglob("*.pdf")):
        yield item


def convert_with_docling(path: Path) -> str | None:
    try:
        from docling.document_converter import DocumentConverter
    except Exception:
        return None

    converter = DocumentConverter()
    result = converter.convert(str(path))
    document = result.document
    if hasattr(document, "export_to_markdown"):
        return document.export_to_markdown()
    return str(document)


def convert_with_pymupdf(path: Path) -> tuple[str, list[dict]]:
    import fitz

    doc = fitz.open(path)
    pages = []
    chunks = []
    for index, page in enumerate(doc, start=1):
        text = page.get_text("text")
        pages.append({"page": index, "chars": len(text)})
        chunks.append(f"\n\n## Page {index}\n\n{text.strip()}\n")
    return "".join(chunks), pages


def ingest_pdf(path: Path, out_dir: Path) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = path.stem
    md_path = out_dir / f"{stem}.md"
    meta_path = out_dir / f"{stem}.json"

    markdown = convert_with_docling(path)
    engine = "docling"
    pages = []
    if markdown is None:
        markdown, pages = convert_with_pymupdf(path)
        engine = "pymupdf"

    md_path.write_text(f"# {path.name}\n\n{markdown}", encoding="utf-8")
    meta = {
        "source_file": str(path),
        "engine": engine,
        "markdown": str(md_path),
        "pages": pages,
    }
    meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
    return meta


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert PDFs to Markdown for AX knowledge ingestion.")
    parser.add_argument("input", type=Path)
    parser.add_argument("--out", type=Path, default=Path("data/processed/pdf"))
    args = parser.parse_args()

    summaries = [ingest_pdf(pdf, args.out) for pdf in iter_pdfs(args.input)]
    summary_path = args.out / "ingest_summary.json"
    summary_path.write_text(json.dumps(summaries, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Processed {len(summaries)} PDF(s). Summary: {summary_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

