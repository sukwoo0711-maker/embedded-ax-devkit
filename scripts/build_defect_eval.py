from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert defect_case.yaml into JSONL eval cases.")
    parser.add_argument("--defects", type=Path, default=Path("templates/defect_case.yaml"))
    parser.add_argument("--out", type=Path, default=Path("knowledge/defect_eval_cases.jsonl"))
    args = parser.parse_args()

    data = yaml.safe_load(args.defects.read_text(encoding="utf-8")) or {}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with args.out.open("w", encoding="utf-8") as out:
        for defect in data.get("defects", []):
            eval_block = defect.get("eval") or {}
            case = {
                "id": defect.get("id"),
                "category": defect.get("category"),
                "input": eval_block.get("input"),
                "expected_finding": eval_block.get("expected_finding"),
                "prevention_rule": defect.get("prevention_rule"),
                "root_cause": defect.get("root_cause"),
                "missed_reason": defect.get("missed_reason"),
            }
            if case["id"] and case["input"] and case["expected_finding"]:
                out.write(json.dumps(case, ensure_ascii=False) + "\n")
                count += 1

    print(f"Wrote {count} defect eval case(s) to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

