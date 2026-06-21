from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Iterable

import pandas as pd
import yaml


def iter_logs(path: Path) -> Iterable[Path]:
    if path.is_file():
        yield path
        return
    for item in sorted(path.rglob("*")):
        if item.suffix.lower() in {".csv", ".txt", ".log"}:
            yield item


def parse_key_value_log(path: Path) -> pd.DataFrame:
    rows = []
    pattern = re.compile(r"([A-Za-z_][A-Za-z0-9_]*)=([-+]?\d+(?:\.\d+)?)")
    for line_no, line in enumerate(path.read_text(encoding="utf-8", errors="ignore").splitlines(), start=1):
        pairs = pattern.findall(line)
        if not pairs:
            continue
        row = {key: float(value) for key, value in pairs}
        row["_line"] = line_no
        rows.append(row)
    return pd.DataFrame(rows)


def load_log(path: Path) -> pd.DataFrame:
    if path.suffix.lower() == ".csv":
        return pd.read_csv(path)
    df = parse_key_value_log(path)
    if not df.empty:
        return df
    return pd.read_csv(path, sep=None, engine="python")


def analyze(df: pd.DataFrame, spec: dict) -> dict:
    report: dict = {
        "rows": int(len(df)),
        "columns": list(map(str, df.columns)),
        "warnings": [],
        "ranges": {},
    }

    time_col = "time_ms" if "time_ms" in df.columns else None
    if time_col and len(df) > 2:
        deltas = df[time_col].diff().dropna()
        expected = spec.get("sampling", {}).get("expected_period_ms", 200)
        jitter = spec.get("sampling", {}).get("max_jitter_ms", 50)
        report["sampling"] = {
            "mean_ms": float(deltas.mean()),
            "min_ms": float(deltas.min()),
            "max_ms": float(deltas.max()),
            "expected_ms": expected,
        }
        missing = df.loc[df[time_col].diff() > expected + jitter, time_col].tolist()
        if missing:
            report["warnings"].append({
                "type": "missing_or_delayed_sample",
                "count": len(missing),
                "first_time_ms": missing[0],
            })

    for signal in spec.get("signals", []):
        name = signal.get("name")
        if not name or name not in df.columns:
            if signal.get("required"):
                report["warnings"].append({"type": "missing_required_signal", "signal": name})
            continue
        series = pd.to_numeric(df[name], errors="coerce").dropna()
        if series.empty:
            continue
        report["ranges"][name] = {
            "min": float(series.min()),
            "max": float(series.max()),
            "mean": float(series.mean()),
        }
        valid_range = signal.get("valid_range")
        if valid_range and len(valid_range) == 2:
            low, high = valid_range
            bad = df[(pd.to_numeric(df[name], errors="coerce") < low) | (pd.to_numeric(df[name], errors="coerce") > high)]
            if not bad.empty:
                report["warnings"].append({
                    "type": "range_violation",
                    "signal": name,
                    "count": int(len(bad)),
                })

    numeric = df.select_dtypes(include="number")
    if len(numeric.columns) >= 1 and len(numeric) > 20:
        try:
            import ruptures as rpt

            target_col = "motor_rpm" if "motor_rpm" in numeric.columns else numeric.columns[-1]
            signal = numeric[target_col].fillna(method="ffill").fillna(0).to_numpy()
            algo = rpt.Pelt(model="rbf").fit(signal)
            change_points = algo.predict(pen=10)
            report["change_points"] = {
                "signal": target_col,
                "indexes": [int(x) for x in change_points[:20]],
            }
        except Exception as exc:
            report["warnings"].append({"type": "change_point_detection_failed", "error": str(exc)})

    return report


def write_markdown(path: Path, source: Path, report: dict) -> None:
    lines = [f"# UART Analysis: {source.name}", ""]
    lines.append(f"Rows: {report.get('rows')}")
    lines.append("")
    if "sampling" in report:
        lines.append("## Sampling")
        for key, value in report["sampling"].items():
            lines.append(f"- {key}: {value}")
        lines.append("")
    lines.append("## Warnings")
    if report["warnings"]:
        for warning in report["warnings"]:
            lines.append(f"- `{warning.get('type')}`: {warning}")
    else:
        lines.append("- none")
    lines.append("")
    lines.append("## Ranges")
    for name, stats in report.get("ranges", {}).items():
        lines.append(f"- `{name}`: {stats}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze 200 ms UART logs.")
    parser.add_argument("input", type=Path)
    parser.add_argument("--spec", type=Path, default=Path("templates/uart_signal_spec.yaml"))
    parser.add_argument("--out", type=Path, default=Path("data/processed/uart"))
    args = parser.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)
    spec = yaml.safe_load(args.spec.read_text(encoding="utf-8")) if args.spec.exists() else {}
    summaries = []
    for log_path in iter_logs(args.input):
        df = load_log(log_path)
        report = analyze(df, spec)
        report["source_file"] = str(log_path)
        json_path = args.out / f"{log_path.stem}.analysis.json"
        md_path = args.out / f"{log_path.stem}.analysis.md"
        json_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        write_markdown(md_path, log_path, report)
        summaries.append({"source": str(log_path), "json": str(json_path), "markdown": str(md_path)})

    summary_path = args.out / "uart_analysis_summary.json"
    summary_path.write_text(json.dumps(summaries, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Analyzed {len(summaries)} UART log(s). Summary: {summary_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

