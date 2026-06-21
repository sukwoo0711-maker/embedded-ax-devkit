# 08. Handoff Prompt

내일 다른 PC에서 AI에게 이 repo를 넘길 때 아래 prompt를 사용한다.

```text
다음 private GitHub repo를 기준으로 내 개발 PC에 AX 환경을 이식해줘.

Repo:
https://github.com/sukwoo0711-maker/embedded-ax-devkit

목표:
사내 S/W 사양서, UX PDF/design export, MRT/SRT/과제 사양 Excel, 결함 export, 200 ms UART 로그를
제품개발자 1명이 활용 가능한 AI-assisted refactoring 환경으로 묶는다.

먼저 다음 파일을 읽어라.
1. README.md
2. AGENTS.md
3. docs/00-executive-plan.md
4. docs/02-system-architecture.md
5. docs/03-pc-setup.md
6. docs/04-agent-playbooks.md
7. docs/06-security-and-data-policy.md

주의:
- 사내 원문 자료를 repo에 commit하지 마라.
- data/raw/ 아래에만 원문을 둬라.
- cloud AI에 사내 원문을 올리지 마라. 익명화된 contract와 review bundle만 사용해라.
- 먼저 python venv를 만들고 requirements.txt를 설치한 뒤 scripts/run_smoke.py를 실행해라.
- smoke test가 통과하기 전에는 실제 제품 자료를 넣지 마라.

내 PC 기준:
- RAM 32 GB
- GTX 3050 Ti
- Ollama 사용 가능
- local LLM은 7B급 모델 우선
- Codex는 반복 구현/리뷰에 사용
- Claude Code는 큰 리팩토링 sprint에만 사용

처음 해줄 일:
1. repo clone
2. venv 생성
3. dependency 설치
4. run_smoke.py 통과 확인
5. data/raw 폴더에 어떤 자료를 어떤 이름으로 넣을지 안내
6. 사내 자료 없이도 templates/*.yaml을 내 프로젝트에 맞게 채우는 순서 제안
```

## 사람이 준비할 자료

```text
data/raw/spec_portal/
  spec_page_export_001.pdf
  spec_page_export_002.html

data/raw/ux/
  ux_spec_screen_group_a.pdf
  design_export_sample.json

data/raw/requirements/
  MRT.xlsx
  SRT.xlsx
  project_control_spec.xlsx
  project_performance_spec.xlsx
  project_vibration_spec.xlsx

data/raw/defects/
  defects_recent_6_months.xlsx

data/raw/uart/
  normal_course_a_001.csv
  defect_case_a_001.csv
```

## 첫날 목표

- smoke test 통과
- UX 화면 3개를 `ux_contract.yaml`에 기록
- LCD packet 3개를 `packet_contract.yaml`에 기록
- UART signal 10개를 `uart_signal_spec.yaml`에 기록
- 결함 5개를 `defect_case.yaml`에 기록

