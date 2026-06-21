# 02. System Architecture

## 전체 구조

```text
Raw Sources
  spec portal export / UX PDF / design export / Excel / defects / UART logs
        |
        v
Ingest Layer
  ingest_pdf.py / ingest_excel.py / ingest_figma_export.py / parse_uart_log.py
        |
        v
Contract Layer
  ux_contract.yaml / device_contract.yaml / packet_contract.yaml / scheduler_contract.yaml
        |
        v
Knowledge Layer
  Markdown chunks / JSONL index / local vector DB or cloud file search
        |
        v
Agent Layer
  Codex / Claude Code / local LLM
        |
        v
Verification Layer
  review bundle / defect eval / UART anomaly report / human checklist
```

## 왜 contract layer가 필요한가

사양서와 UX 문서를 그대로 LLM에 넣으면 질문할 때마다 답이 흔들린다. 개발자가 실제로 필요한 것은 다음처럼 판정 가능한 계약이다.

```text
화면 A는 어떤 데이터를 요구하는가
그 데이터는 제품 firmware의 어떤 state에서 오는가
LCD packet의 어떤 field로 나가는가
몇 ms 주기로 갱신되어야 하는가
어떤 결함이 과거에 있었는가
UART 로그에서 어떤 signal로 검증되는가
```

## 데이터 흐름

### S/W 사양 포털

1. 사람이 필요한 spec page를 HTML/PDF/Markdown으로 export한다.
2. `data/raw/spec_portal/`에 저장한다.
3. `ingest_pdf.py` 또는 Markdown copy로 `data/processed/spec_portal/*.jsonl`을 만든다.
4. AI는 원문 page id와 section id를 인용해야 한다.

### UX 사양

1. UX PDF는 `ingest_pdf.py`로 Markdown/JSON 변환한다.
2. 디자인 도구 export JSON은 `ingest_figma_export.py`로 screen/component 후보를 만든다.
3. 제품개발자는 `ux_contract.yaml`에 screen별 required data를 확정한다.

### LCD packet

1. LCD S/W팀과 협의한 field를 `packet_contract.yaml`에 기록한다.
2. firmware 변경 시 packet field 추가/삭제/scale/unit 변경을 AI가 리뷰한다.
3. 결함 발생 시 packet field와 UX required data를 먼저 대조한다.

### Excel 요구사항

1. MRT/SRT/과제 사양 Excel을 `ingest_excel.py`로 JSONL과 Markdown table로 변환한다.
2. `requirement_trace.yaml`에 제품 공통 표준사양과 과제별 override를 연결한다.
3. AI는 "국내/미국 차이" 같은 변형 요구사항을 source row와 함께 설명한다.

### 결함

1. 결함 export를 `data/raw/defects/`에 둔다.
2. 자주 발생하는 결함을 `defect_case.yaml`로 축약한다.
3. 각 결함은 review rule과 eval case로 전환한다.

### UART 로그

1. 200 ms 로그를 `data/raw/uart/`에 둔다.
2. `parse_uart_log.py`가 sampling period, missing sample, signal range, phase transition 후보를 뽑는다.
3. 사양 기반 signal expectation은 `uart_signal_spec.yaml`에 둔다.
4. 품질팀이 보던 그래프는 자동 후보 표시 리포트로 바꾼다.

## Agent 권한 분리

| Agent | 허용 | 금지 |
| --- | --- | --- |
| Local LLM | 사내 자료 질의, 요약 초안, 민감 문서 탐색 | 코드 자동 수정, merge 판단 |
| Codex | repo 분석, 리팩토링 제안/구현, script 개선 | 사양 근거 없는 behavior 추가 |
| Claude Code | 큰 리팩토링 sprint, 복잡한 코드 이해 | 장기 기억 역할, 무검증 대량 변경 |
| Deterministic scripts | Excel/PDF/log 변환, UART anomaly 후보 | 최종 결함 판정 |

