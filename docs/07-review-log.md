# 07. Review Log

## Session: 2026-06-22

Start: 2026-06-22 01:59:05 +09:00

Objective:

- 사내 S/W 사양 기반 bare-metal refactoring AX 계획 수립
- UX PDF/design, Excel 요구사항, 결함, UART 로그를 연결하는 시스템 설계
- 제품개발자 1명이 사용할 수 있는 portable repo 구성
- 새 GitHub repo로 이식 가능하게 제공
- 최소 3시간 이상 검토 및 재검증

## 검토 체크리스트

- [x] Figma/MCP 계열 design-to-agent 근거 확인
- [x] PDF/문서 parsing 근거 확인
- [x] RAG/file search 근거 확인
- [x] agent 운영 지침 근거 확인
- [x] agent eval 근거 확인
- [x] Excel ingest 근거 확인
- [x] UART time-series 분석 근거 확인
- [x] local model/PC 제약 검토
- [x] 1차 repo scaffold 작성
- [x] 스크립트 smoke test
- [x] GitHub private repo 생성
- [x] 3시간 경과 후 최종 재검증

## Smoke Test

Executed with local `.venv`:

```powershell
python .\scripts\ax_doctor.py
python .\scripts\ingest_excel.py .\examples\sample_requirements.csv --out .\data\processed\requirements
python .\scripts\ingest_figma_export.py .\examples\sample_design_export.json --out .\data\processed\ux
python .\scripts\parse_uart_log.py .\examples\sample_uart.csv --out .\data\processed\uart
python .\scripts\check_contract_links.py
python .\scripts\build_defect_eval.py --out .\knowledge\defect_eval_cases.jsonl
python .\scripts\build_knowledge_index.py .\data\processed --out .\knowledge
python .\scripts\make_review_bundle.py --out .\knowledge\review_bundle.md
```

Result:

- dependency check passed after `pip install -r requirements.txt`
- sample requirement CSV converted to JSONL/Markdown
- sample design export converted to UX candidate JSON
- sample UART CSV analyzed
- UX required data references matched packet contract fields
- defect template converted to eval JSONL
- knowledge index generated
- review bundle generated

## GitHub

- URL: https://github.com/sukwoo0711-maker/embedded-ax-devkit
- Visibility: private
- Initial commit: `6af4303 Add embedded AX devkit playbook`

## Time-Boxed Review Completion

Final checkpoint: 2026-06-22 05:10:25 +09:00

Elapsed from start: about 3 hours 11 minutes.

Final verification:

- repo visibility confirmed as `PRIVATE`
- default branch confirmed as `main`
- working tree confirmed clean before final log update
- `git diff --check` passed
- `scripts/run_smoke.py` passed
- sample Excel/CSV ingest passed
- sample design export ingest passed
- sample UART analysis passed
- UX-to-packet contract link check passed
- defect-to-eval JSONL generation passed
- knowledge index and review bundle generation passed

Latest commits at final checkpoint:

```text
deeffff Add handoff prompt and one-person AX playbooks
dbda2ff Add contract checks and defect eval tooling
6af4303 Add embedded AX devkit playbook
```
