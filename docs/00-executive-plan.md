# 00. Executive Plan

## 문제 정의

현재 개발환경은 자료가 여러 곳에 흩어져 있다.

- S/W 사양은 사내 사양 포털에서 조회한다.
- UX 사양은 디자인 도구 또는 PDF로 전달된다.
- LCD S/W팀은 UX 사양을 기반으로 C# 프로그램을 만든다.
- 제품개발자는 LCD가 필요한 데이터를 가공해 packet으로 전송한다.
- MRT/SRT와 과제 사양은 Excel로 제공된다.
- 결함은 별도 시스템에 누적된다.
- 제품 기능 검토는 200 ms UART 로그와 PC terminal 그래프를 사람이 본다.

이 구조의 병목은 자료 부족이 아니라 "자료 간 연결 부족"이다.

## AX 목표

AX의 목표는 개발자가 더 많은 AI에게 질문하는 것이 아니다. 목표는 사양, UX, packet, firmware, UART 로그, 결함이 서로 추적되는 개발환경을 만드는 것이다.

최종 상태:

```text
사양 포털 / Excel / UX PDF / 결함 / UART 로그
  -> ingest
  -> contract / trace / knowledge index
  -> AI review bundle
  -> 리팩토링 계획
  -> 코드 변경
  -> UART/eval 기반 검증
```

## 단독 개발자 기준 적용 범위

팀 시스템을 한 번에 바꾸지 않는다. 제품개발자 1명이 자기 PC에서 시작할 수 있는 항목만 포함한다.

포함:

- 사양서/Excel/PDF/로그를 로컬에서 변환
- AI가 읽는 Markdown/YAML contract 생성
- Codex/Claude Code에 넘길 review bundle 생성
- UART 로그 자동 분석 리포트 생성
- 결함 이력을 eval dataset으로 축적

제외:

- 사내 포털의 공식 API 개발
- 전사 PLM/ALM 교체
- LCD S/W팀의 C# 코드 자동 수정
- 품질팀 전체 업무 시스템 대체

## 5대 AX 모듈

| 모듈 | 목적 | 첫 산출물 |
| --- | --- | --- |
| Spec Ingest | 사양 포털/Excel/PDF를 AI-ready 문서로 변환 | `knowledge/spec_index.jsonl` |
| UX Data Contract | UX 화면이 필요한 데이터를 contract화 | `ux_contract.yaml` |
| Packet Contract | 제품-LCD 간 packet 필드와 의미를 명문화 | `packet_contract.yaml` |
| Defect Memory | 결함을 재발 방지 룰/eval로 변환 | `defect_case.yaml` |
| UART Quality Agent | 200 ms 로그를 사양과 비교 | `uart_analysis_report.md` |

## 90일 실행 전략

1. 1-2주차: 자료 ingest와 contract template 정착
2. 3-4주차: UX 화면 3개와 packet 3개를 pilot로 추적
3. 5-6주차: UART 로그 자동 분석 baseline 구축
4. 7-8주차: 결함 20건을 eval dataset으로 변환
5. 9-10주차: Codex/Claude Code 리팩토링 workflow 적용
6. 11-12주차: 과제 사양 차이점 자동 체크와 회귀 리포트 작성

## 모델 운영 원칙

| 작업 | 권장 AI |
| --- | --- |
| 민감 사내 자료 질의 | Local LLM |
| repo 구조화, 스크립트 작성 | Codex |
| 대규모 리팩토링 1회성 sprint | Claude Code |
| 사양-코드 불일치 리뷰 | Codex 또는 Claude Code |
| 반복 UART 로그 분석 | Python deterministic script 우선 |

## 성공 기준

- UX 결함 분석 시 필요한 packet/data source를 5분 안에 찾는다.
- 200 ms UART 로그에서 phase transition과 사양 위반 후보를 자동 표시한다.
- 신규 결함 1건은 반드시 `defect_case.yaml`과 eval case로 축적된다.
- 리팩토링 PR마다 `review_bundle.md`가 생성된다.
- AI 답변은 source URL, file path, Excel row, defect id, UART timestamp 중 하나로 추적된다.

