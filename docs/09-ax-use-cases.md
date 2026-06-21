# 09. AX Use Cases For One Product Developer

## 1. UX 화면 필요 데이터 자동 색인

입력:

- UX PDF 또는 design export
- LCD packet contract

출력:

- 화면별 required data 후보
- packet field mapping 후보
- LCD S/W팀에 질문할 누락 field 목록

효과:

- "이 화면을 구성하려면 어떤 데이터를 보내야 하지?"를 빠르게 찾는다.

## 2. LCD 표시 결함 1차 triage

입력:

- 결함 내용
- UX contract
- packet contract
- UART 로그

출력:

- 제품 firmware 전송 문제 후보
- LCD S/W 분석 대상 후보
- 추가로 필요한 로그/field

효과:

- 제품개발자와 LCD S/W팀 사이의 책임 구분 시간이 줄어든다.

## 3. Packet scale/unit 변경 감시

입력:

- packet contract
- 변경 diff

출력:

- enum/unit/scale/period 변경 경고
- LCD S/W 협의 필요 항목

효과:

- "값은 보냈는데 LCD가 다르게 표시"되는 결함을 줄인다.

## 4. Superloop 주기 위반 리뷰

입력:

- scheduler contract
- firmware diff

출력:

- 50 ms 함수가 100 ms task에서만 호출되는 구조
- timeout tick 단위 불일치
- static state update period mismatch

효과:

- bare-metal refactoring 중 숨어 있는 timing regression을 잡는다.

## 5. 표준사양 vs 과제사양 override table

입력:

- 표준사양
- 과제 사양 Excel
- 제품 variant

출력:

- 공통 behavior
- variant-specific behavior
- 코드 조건문 분리 후보

효과:

- 국내/미국 등 파생 제품 차이를 코드에 흩뿌리지 않고 구조화한다.

## 6. UART 200 ms 로그 자동 품질 검토

입력:

- UART CSV/TXT
- uart signal spec

출력:

- missing sample
- signal range violation
- phase transition 후보
- 급수/모터/온도 profile 위반 후보

효과:

- 품질팀이 그래프 전체를 일일이 보는 대신, 이상 후보를 먼저 본다.

## 7. 결함 이력 기반 AI reviewer 훈련

입력:

- defect case

출력:

- eval JSONL
- review rule
- expected finding

효과:

- 한 번 놓친 유형을 다음 PR에서 다시 묻는다.

## 8. 리팩토링 전 behavior table 생성

입력:

- 사양 index
- 코드 path
- 제품 variant

출력:

- 현재 behavior table
- 변경 후 behavior table
- risk list

효과:

- AI가 코드를 바꾸기 전에 사람이 behavior를 확인할 수 있다.

## 9. LCD S/W팀 협의 bundle 생성

입력:

- UX contract
- packet contract
- defect case
- sample UART log

출력:

- "제품은 이 field를 이 값/주기로 보냈다" bundle
- "LCD에서 확인할 expected rendering" checklist

효과:

- 팀 간 로그 분석 대화가 짧아진다.

## 10. Cloud AI 사용 전 익명화 bundle 생성

입력:

- contract YAML
- 관련 코드 diff
- 결함 요약

출력:

- 사내 원문 제거된 review bundle

효과:

- Codex/Claude Code를 쓰면서도 사내 원문 노출을 줄인다.

