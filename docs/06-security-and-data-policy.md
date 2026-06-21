# 06. Security And Data Policy

## 원칙

이 repo는 playbook과 도구만 담는다. 사내 원문은 담지 않는다.

## 금지 데이터

- 사내 포털 계정/쿠키/token
- 제품명, 프로젝트명, 고객명
- 공개 금지 사양 원문
- 결함 시스템 개인 정보
- UART 로그 중 민감 식별자

## 허용 데이터

- 익명화된 sample schema
- 빈 template
- 변환 script
- 공개 문서 URL
- 사내 이식 절차

## Cloud AI 사용 기준

| 자료 | Local LLM | Codex/Claude Code cloud |
| --- | --- | --- |
| 공개 문서 | 허용 | 허용 |
| 사내 사양 원문 | 허용 | 원칙적으로 금지 또는 승인 필요 |
| 익명화된 contract | 허용 | 허용 |
| 결함 원문 | 허용 | 익명화 후만 허용 |
| UART raw log | 허용 | 제품/고객 식별 제거 후만 허용 |

## 익명화 규칙

- 제품명은 `PRODUCT_A`
- 국가/파생 모델은 `REGION_A`, `REGION_B`
- 결함 번호는 내부 보관용과 외부 공유용을 분리
- 개인 이름은 제거
- absolute path는 제거

## AI session log

AI에게 사내 자료를 읽혔다면 다음을 기록한다.

```yaml
date: 2026-06-22
agent: local-llm
sources:
  - data/raw/spec_portal/...
task: "UX packet triage"
output: "data/processed/..."
human_reviewed_by: ""
cloud_shared: false
```

