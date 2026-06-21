# 04. Agent Playbooks

## Playbook A: UX 표시 결함 triage

상황: "LCD 표시가 올바르지 않다"는 결함이 등록되었다.

절차:

1. 결함 id, 화면명, 재현 조건, 제품 variant를 기록한다.
2. `ux_contract.yaml`에서 해당 screen의 required data를 찾는다.
3. `packet_contract.yaml`에서 LCD packet field와 unit/scale/update period를 찾는다.
4. firmware에서 field 생성 위치를 찾는다.
5. UART 로그에 동일 data가 있으면 timestamp와 값을 비교한다.
6. 제품개발자 packet 문제가 아니면 LCD S/W팀 분석용 bundle을 만든다.

AI에게 요청:

```text
AGENTS.md를 읽고, defect id X의 UX 표시 문제를 triage해줘.
ux_contract.yaml, packet_contract.yaml, 관련 UART log, defect_case.yaml을 근거로
제품 firmware 문제인지 LCD S/W팀 분석으로 넘겨야 하는지 판단 후보를 작성해.
단정하지 말고 필요한 추가 로그를 알려줘.
```

## Playbook B: 과제 사양 기반 리팩토링

상황: 표준사양은 같지만 국가/파생 제품별 동작이 다르다.

절차:

1. `requirement_trace.yaml`에 표준사양과 과제 override를 등록한다.
2. 코드에서 제품 variant 조건문을 찾는다.
3. 공통 동작과 variant 동작을 분리한다.
4. AI에게 리팩토링 전에 behavior table을 만들게 한다.
5. 사람이 table을 승인한 후 코드 변경한다.

AI에게 요청:

```text
이 리팩토링은 과제 사양 override를 코드 구조로 분리하는 작업이다.
먼저 현재 behavior table을 만들어라.
그 다음 표준사양과 과제사양의 차이만 분리하는 최소 변경 계획을 세워라.
scheduler, packet format, calibration constant는 승인 전 변경하지 마라.
```

## Playbook C: UART 200 ms 품질 검토 자동화

상황: 품질팀이 PC terminal graph를 보고 수동 검토한다.

절차:

1. `uart_signal_spec.yaml`에 signal, unit, expected range, phase rule을 정의한다.
2. `parse_uart_log.py`로 sampling period와 missing samples를 검사한다.
3. phase transition 후보를 찾는다.
4. 사양상 start 이후 급수/모터/온도 profile과 비교한다.
5. anomaly 후보만 사람이 본다.

AI에게 요청:

```text
UART 분석 리포트를 보고 사양 위반 후보를 분류해줘.
결함이라고 단정하지 말고, 어떤 사양/phase/log timestamp를 확인해야 하는지 목록화해줘.
```

## Playbook D: 결함을 eval로 바꾸기

상황: 과거 결함이 반복된다.

절차:

1. 결함 원인, 놓친 이유, 재발 방지 관점을 `defect_case.yaml`에 기록한다.
2. AI reviewer가 같은 유형을 잡아야 하는 질문을 만든다.
3. 정답 기준을 사람이 작성한다.
4. 다음 PR review 때 eval case로 사용한다.

예:

```yaml
id: DEFECT-UX-001
missed_reason: "packet scale changed but LCD contract not updated"
review_rule: "packet field scale/unit 변경 시 LCD consumer contract도 변경되어야 한다"
expected_ai_finding: "scale/unit mismatch risk"
```

## Playbook E: Codex/Claude Code 리팩토링 sprint

준비물:

- `review_bundle.md`
- 관련 contract YAML
- defect eval 최소 20건
- UART baseline log
- 현재 코드의 test/build 방법

요청 순서:

1. 코드 변경 없이 architecture와 risk를 요약하게 한다.
2. behavior table을 만들게 한다.
3. 변경 계획을 파일 단위로 나누게 한다.
4. 작은 commit 단위로 구현하게 한다.
5. deterministic script와 사람이 확인할 checklist를 실행한다.

