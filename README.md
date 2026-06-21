# Embedded AX Devkit

사내 S/W 사양서, UX 사양서, 결함, UART 로그를 바탕으로 bare-metal 임베디드 개발자의 AX(AI Transformation)를 구축하기 위한 portable playbook이다.

이 저장소는 실제 사내 자료를 포함하지 않는다. 다른 PC로 이식할 때는 `data/raw/`에 사양서 export, UX PDF, Excel 요구사항, 결함 export, UART 로그를 넣고 `scripts/`를 실행한다.

## 목표

제품개발자 1명이 다음 작업을 더 빠르고 일관되게 수행하도록 돕는다.

- 사내 사양 포털의 S/W 사양서를 내부 지식으로 정리
- UX팀의 디자인/PDF 사양에서 화면별 필요 데이터 추출
- LCD S/W팀과 주고받는 packet/data contract 명문화
- MRT/SRT 및 과제 사양 Excel을 요구사항 trace로 변환
- 결함 이력을 AI reviewer/eval dataset으로 재사용
- 200 ms UART 로그를 자동 분석해 품질 검출력 향상
- Codex/Claude Code/local LLM을 역할별로 나누어 사용

## 빠른 시작

```powershell
git clone <THIS_REPO_URL> C:\GitRepositories\embedded-ax-devkit
cd C:\GitRepositories\embedded-ax-devkit
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python .\scripts\ax_doctor.py
```

자료를 넣는 위치:

```text
data/raw/spec_portal/       # 사내 S/W 사양서 export HTML/PDF/MD
data/raw/ux/                # UX PDF 또는 디자인 도구 export JSON
data/raw/requirements/      # MRT/SRT/과제 사양 Excel
data/raw/defects/           # 결함 export CSV/XLSX
data/raw/uart/              # 200 ms UART log CSV/TXT
```

최소 ingest:

```powershell
python .\scripts\ingest_excel.py .\data\raw\requirements --out .\data\processed\requirements
python .\scripts\ingest_pdf.py .\data\raw\ux --out .\data\processed\ux
python .\scripts\parse_uart_log.py .\data\raw\uart --out .\data\processed\uart
python .\scripts\build_knowledge_index.py .\data\processed --out .\knowledge
```

샘플 smoke test:

```powershell
python .\scripts\run_smoke.py
```

## 저장소 지도

```text
embedded-ax-devkit/
  AGENTS.md
  README.md
  requirements.txt
  docs/
    00-executive-plan.md
    01-evidence-map.md
    02-system-architecture.md
    03-pc-setup.md
    04-agent-playbooks.md
    05-implementation-roadmap.md
    06-security-and-data-policy.md
    07-review-log.md
  templates/
    ux_contract.yaml
    device_contract.yaml
    packet_contract.yaml
    scheduler_contract.yaml
    requirement_trace.yaml
    defect_case.yaml
    uart_signal_spec.yaml
  scripts/
    ax_doctor.py
    ingest_excel.py
    ingest_pdf.py
    ingest_figma_export.py
    parse_uart_log.py
    build_knowledge_index.py
    make_review_bundle.py
```

## 권장 운용

1. Codex는 repo 이해, 리팩토링 계획, 스크립트 수정, review bundle 작성에 사용한다.
2. Claude Code는 큰 리팩토링 1회성 sprint에 사용하되, 반드시 `AGENTS.md`와 contract를 먼저 읽게 한다.
3. Local LLM은 사내 자료 질의, 요약 초안, 민감 자료 탐색에 사용한다.
4. AI가 만든 모든 결론은 원본 사양 page, Excel row, defect id, UART timestamp로 되돌아갈 수 있어야 한다.
5. merge 전에는 사람이 `packet_contract.yaml`, `scheduler_contract.yaml`, UART 분석 결과를 확인한다.

## 핵심 원칙

AI에게 제품을 맡기지 않는다. AI에게 사양과 구현 사이의 불일치를 계속 찾게 한다.
