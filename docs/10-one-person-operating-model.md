# 10. One-Person Operating Model

## 매일

1. 개발 전 관련 사양/UX/packet contract를 확인한다.
2. AI에게 바로 코드 작성을 시키지 말고 behavior table을 먼저 만들게 한다.
3. 변경 후 `check_contract_links.py`와 관련 smoke check를 실행한다.
4. UART 로그가 있으면 `parse_uart_log.py`로 후보 이상을 본다.
5. 결함 또는 놓친 점은 `defect_case.yaml`에 남긴다.

## 매주

1. 새로 받은 사양서/Excel/PDF를 ingest한다.
2. contract YAML을 갱신한다.
3. defect eval을 갱신한다.
4. Codex budget으로 script와 review bundle을 개선한다.
5. Claude Code budget은 아낀다.

## 리팩토링 sprint 전

1. 대상 feature의 표준사양과 과제사양을 모두 모은다.
2. UX 화면과 packet mapping을 확정한다.
3. scheduler contract에서 task/function period를 확정한다.
4. 최근 결함 20개를 eval case로 만든다.
5. 정상 UART log와 결함 UART log를 준비한다.
6. 그 다음 Claude Code로 큰 구조 변경을 맡긴다.

## 리뷰 질문 template

```text
AGENTS.md와 review_bundle.md를 기준으로 이 변경을 리뷰해줘.
중점은 다음이다.

1. 사양과 behavior 불일치
2. UX required data와 packet field 불일치
3. packet unit/scale/period 변경 위험
4. superloop task period와 function required_period 불일치
5. 과거 defect_case.yaml의 재발 가능성
6. UART 로그로 검증해야 할 signal

결함이라고 단정하지 말고, MUST_FIX / SHOULD_CHECK / INFO로 나눠라.
각 항목마다 source file, contract id, requirement id, defect id, UART timestamp 중 하나를 붙여라.
```

## 사람의 최종 판단

AI가 잘하는 것:

- 흩어진 자료 연결
- 누락 후보 탐지
- 리뷰 체크리스트 생성
- 반복 로그 분석 후보 표시

AI에게 맡기면 안 되는 것:

- 안전/규격 최종 판단
- 사양 해석 최종 승인
- LCD S/W팀과 합의된 protocol 변경
- calibration 및 register-level 변경
- 결함 root cause 확정

