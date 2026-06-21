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
- [ ] GitHub private repo 생성
- [ ] 3시간 경과 후 최종 재검증

## Smoke Test

Executed with local `.venv`:

```powershell
python .\scripts\ax_doctor.py
python .\scripts\ingest_excel.py .\examples\sample_requirements.csv --out .\data\processed\requirements
python .\scripts\ingest_figma_export.py .\examples\sample_design_export.json --out .\data\processed\ux
python .\scripts\parse_uart_log.py .\examples\sample_uart.csv --out .\data\processed\uart
python .\scripts\build_knowledge_index.py .\data\processed --out .\knowledge
python .\scripts\make_review_bundle.py --out .\knowledge\review_bundle.md
```

Result:

- dependency check passed after `pip install -r requirements.txt`
- sample requirement CSV converted to JSONL/Markdown
- sample design export converted to UX candidate JSON
- sample UART CSV analyzed
- knowledge index generated
- review bundle generated

