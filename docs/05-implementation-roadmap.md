# 05. Implementation Roadmap

## Phase 0: 하루 안에 준비

- 이 repo를 clone한다.
- Python venv를 만든다.
- `ax_doctor.py`를 실행한다.
- `run_smoke.py`를 실행해 샘플 파이프라인을 검증한다.
- 사내 자료 원문은 commit하지 않는다는 원칙을 확인한다.

## Phase 1: 1주차

목표: 자료를 AI가 읽을 수 있게 바꾼다.

- 사양 포털에서 핵심 spec 5개를 export한다.
- UX PDF 1개를 `ingest_pdf.py`로 변환한다.
- MRT/SRT Excel 1개를 `ingest_excel.py`로 변환한다.
- UART 로그 3개를 `parse_uart_log.py`로 분석한다.

완료 기준:

- `knowledge/index.jsonl` 생성
- `ux_contract.yaml` 화면 3개 작성
- `packet_contract.yaml` packet 3개 작성

## Phase 2: 2-4주차

목표: UX 표시 결함 triage 시간을 줄인다.

- 최근 UX 표시 결함 10건을 `defect_case.yaml`로 기록한다.
- 각 결함에 필요한 packet field를 연결한다.
- LCD S/W팀에 넘길 분석 bundle format을 고정한다.

완료 기준:

- 결함 10건 재현/원인/필요 데이터 trace
- AI가 "제품 packet 문제인지 LCD 분석 대상인지" 후보를 제시

## Phase 3: 5-8주차

목표: UART 품질검토를 사람 그래프 보기에서 후보 자동 검출로 바꾼다.

- 코스별 expected phase를 `uart_signal_spec.yaml`에 정의한다.
- start button 이후 급수, 모터, drain, temperature profile을 rule로 만든다.
- 정상 로그 10개, 결함 로그 10개로 baseline을 만든다.

완료 기준:

- missing sample, range violation, change point, phase duration 후보 자동 표시
- 품질팀 수동 검토 포인트가 report에 정리됨

## Phase 4: 9-12주차

목표: 사양 기반 리팩토링에 AI를 투입한다.

- 표준사양 vs 과제사양 override table 작성
- variant 조건문 정리
- Codex로 작은 리팩토링 반복
- Claude Code budget은 큰 구조 변경 1회에만 사용

완료 기준:

- 리팩토링 PR마다 `review_bundle.md`
- 결함 eval 20건 통과
- UART baseline regression report 첨부
