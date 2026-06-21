# 03. Developer PC Setup

## 기준 PC

- RAM: 32 GB
- GPU: GTX 3050 Ti
- Local LLM: 현재 Qwen 7B 계열 사용 가능
- Cloud budget: Codex weekly 130 USD, Claude Code one-time 1000 USD

## 권장 모델 운영

| 용도 | 권장 | 이유 |
| --- | --- | --- |
| 로컬 사내 문서 질의 | `qwen2.5-coder:7b` 또는 동급 7B instruct/coder | 32K context와 4.7 GB급 모델 크기로 laptop에서 현실적 |
| 빠른 요약/초안 | 7B local model | 민감 자료 외부 반출 방지 |
| 코드 리팩토링 계획 | Codex | repo 작업, 파일 편집, 테스트에 강함 |
| 대규모 1회 리팩토링 | Claude Code | 긴 code context와 강한 reasoning을 budget sprint로 사용 |
| 반복 로그 분석 | Python scripts | LLM보다 재현성과 속도가 중요 |

## 설치

```powershell
cd C:\GitRepositories\embedded-ax-devkit
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python .\scripts\ax_doctor.py
```

샘플 검증:

```powershell
python .\scripts\ingest_excel.py .\examples\sample_requirements.csv --out .\data\processed\requirements
python .\scripts\ingest_figma_export.py .\examples\sample_design_export.json --out .\data\processed\ux
python .\scripts\parse_uart_log.py .\examples\sample_uart.csv --out .\data\processed\uart
python .\scripts\build_knowledge_index.py .\data\processed --out .\knowledge
python .\scripts\make_review_bundle.py --out .\knowledge\review_bundle.md
```

## Ollama 예시

```powershell
ollama pull qwen2.5-coder:7b
ollama run qwen2.5-coder:7b
```

3050 Ti의 VRAM이 부족하면 CPU/RAM offload가 발생한다. 이 경우 local LLM은 코드 작성보다 "사내 문서 검색/요약"에 제한하고, 실제 코드 변경은 Codex/Claude Code에 맡긴다.

## Cloud budget 사용법

### Codex weekly 130 USD

반복적인 작업에 사용한다.

- repo 구조 개선
- ingest script 수정
- review bundle 생성
- 작은 리팩토링
- 테스트 추가

### Claude Code one-time 1000 USD

한 번 크게 써야 하는 sprint에 사용한다.

1. contract와 사양 index를 먼저 완성한다.
2. defect eval 20건 이상을 만든다.
3. UART baseline log를 준비한다.
4. 그 다음 큰 리팩토링을 맡긴다.

준비 없이 Claude Code budget을 쓰면 "그럴듯한 대규모 변경"만 남을 위험이 크다.

## 권장 폴더 배치

```text
C:\GitRepositories\
  embedded-ax-devkit\
  product-firmware\
  lcd-interface-docs\
  private-spec-export\
```

`embedded-ax-devkit`에는 사내 원문을 commit하지 않는다. 원문은 `.gitignore` 처리된 `data/raw/`나 별도 private 폴더에 둔다.
