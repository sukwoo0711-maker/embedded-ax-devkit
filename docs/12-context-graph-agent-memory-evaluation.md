# 12. Context Graph / Agent Memory Evaluation

검증일: 2026-06-25

## 결론

지금 이 devkit에 Neo4j Agent Memory 또는 Create Context Graph를 바로 핵심 런타임으로 붙이는 것은 권장하지 않는다. 현재 이 레포의 목표는 1인 제품 개발자가 사내 S/W 사양, UX, packet, UART, defect 근거를 빠르게 연결하는 것이고, 이미 Markdown/YAML contract와 deterministic script 흐름이 더 가볍고 검증 가능하다.

다만 영상의 핵심 개념인 decision trace, provenance, short/long/reasoning memory는 이 devkit에 유익하다. 즉, 당장은 Neo4j 앱을 도입하지 말고 다음 세 가지를 가볍게 흡수하는 것이 낫다.

1. defect memory에 "어떤 근거와 도구 호출로 판단했는가"를 decision trace로 남긴다.
2. review bundle에 `source -> contract -> signal -> defect -> decision` 경로를 명시한다.
3. 나중에 Neo4j pilot을 할 때는 기존 YAML을 graph import의 원천으로 삼고, raw private source를 직접 넣지 않는다.

## 조사한 자료

| 자료 | 확인 내용 | 판단 |
| --- | --- | --- |
| YouTube `Context Graphs and Agent Memory` | 자동 한국어 자막 기준, context graph는 대화, 엔티티, 사용자 선호, agent tool call, reasoning path를 그래프로 저장해 현재 질문에 필요한 subgraph를 꺼내 쓰자는 내용이다. 영상은 short-term, long-term, reasoning memory의 3계층을 설명한다. | devkit의 "근거 추적" 방향과 잘 맞는다. 단, 영상은 개념 1편에 가깝고 production 도입 검증은 별도다. |
| https://github.com/neo4j-labs/agent-memory | Neo4j 기반 agent memory SDK. Python/TypeScript SDK, NAMS hosted backend, self-hosted bolt backend, MCP server, framework integration, entity extraction, reasoning trace, eval harness를 제공한다. GitHub 기준 Apache-2.0, Experimental/Community Supported, 2026-06-25 조사 시점 public repo다. | 기능 표면은 강하지만 DB와 memory backend가 전제다. 이 devkit의 첫 도입 대상으로는 무겁다. |
| https://github.com/neo4j-labs/create-context-graph | FastAPI + Next.js + Neo4j + agent framework 앱을 scaffold한다. 27개 domain, SaaS connector, decision trace viewer, graph visualization을 생성한다. | 데모/프로토타입에는 유용하다. 이 repo에 바로 scaffold 결과물을 넣는 것은 과하다. |
| https://github.com/getzep/graphiti | temporal context graph. fact validity window, provenance, hybrid retrieval, MCP server를 강조한다. | 장기적으로 더 강력할 수 있지만 운영 부담은 더 크다. 지금은 비교 참고만 하고 설치 검증 대상에서 제외했다. |

## 로컬 검증

환경:

- `uv 0.11.21`
- `gh 2.92.0`
- `node v22.23.0`
- Docker: 설치되지 않음
- PowerShell에서 `npm.ps1`은 실행 정책에 막힘. 필요 시 `npm.cmd` 사용 가능

실행 결과:

| 검증 | 결과 | 의미 |
| --- | --- | --- |
| `uvx create-context-graph --version` | `0.13.1` 실행 성공 | CLI는 설치 없이 실행 가능하다. |
| `uvx create-context-graph --list-domains` | `manufacturing`, `software-engineering`, `agent-memory` 등 27개 domain 확인 | embedded AX에 가까운 후보 domain은 있지만 그대로 맞지는 않는다. |
| `create-context-graph ... --domain manufacturing --framework pydanticai --self-hosted --demo-data` | 첫 실행은 Windows cp949 `UnicodeDecodeError` 실패. `$env:PYTHONUTF8='1'` 설정 후 성공 | Windows 사용자는 UTF-8 강제가 사실상 필요하다. |
| scaffold 산출물 | 55 entities, 84 relationships, 25 documents, 10 decision traces 생성 | decision trace 구조는 참고 가치가 있다. |
| 생성 backend 설치 | `uv sync --extra dev` 성공. 167 packages 설치, `torch`, `spacy`, `sentence-transformers`, `transformers`, `litellm` 포함 | 너무 무겁다. devkit 기본 dependency로 넣으면 안 된다. |
| 생성 backend tests | `uv run python -m pytest tests -v` 결과 2 passed | mock 기반 최소 route 검증은 통과했다. 실제 graph/LLM 동작 검증은 아니다. |
| `neo4j-agent-memory extract` 영어 샘플 | `UX screen`, `water_level_liter`, `MCF8316A controller`, `DEFECT-UX-001`, `1L` 추출. 관계는 없음. `0.1L` 누락 | 영어/식별자 혼합 문장에서는 쓸 수 있지만 contract 수준 자동화로는 부족하다. |
| `neo4j-agent-memory extract` 한국어 샘플 | `MCF8316A`, `water_level_liter`, `1L로` 등 일부만 추출. `DEFECT-UX-001`, `WATER_LEVEL`, `0.1L` 누락. 관계는 없음 | 한국어 사내 문서/결함 요약에 바로 적용하기 어렵다. LLM extractor나 규칙 기반 보정이 필요하다. |

## 엄격한 효용 판단

### 지금 도움이 되는 부분

- "왜 이 결론이 나왔는지"를 reasoning trace로 남기는 습관은 UART/packet/defect triage에 바로 유용하다.
- 단순 vector search보다 `UX screen -> required data -> packet field -> firmware source -> UART signal -> defect` 같은 관계형 질문에 더 잘 맞는다.
- `create-context-graph`가 생성한 ontology, decision trace, graph visualization 구조는 future pilot의 참고 자료로 충분하다.

### 지금 손해가 더 큰 부분

- Docker 또는 Neo4j/Aura/NAMS가 필요하다. 현재 PC에는 Docker가 없다.
- 실제 agent memory 서버를 쓰려면 Neo4j password, NAMS API key, 또는 LLM API key가 필요하다.
- Windows에서는 scaffold에 `PYTHONUTF8=1` 같은 환경 조건이 필요했다.
- local extraction은 한국어와 도메인 식별자에서 누락이 있었다.
- dependency가 무겁다. 단순 문서/contract repo에 넣기에는 설치 비용이 크다.
- Neo4j Labs project는 community supported 성격이라, 1인 제품 개발자의 핵심 workflow에 곧바로 의존하기에는 리스크가 있다.

## 권장 방향

### Adopt now

1. `defect_case.yaml` 또는 review bundle에 decision trace 필드를 추가하는 pilot을 한다.
2. `make_review_bundle.py`가 `evidence_path`를 다음 형태로 출력하게 한다.
   - `spec_page`
   - `ux_screen`
   - `packet_field`
   - `firmware_symbol`
   - `uart_signal`
   - `defect_case`
   - `decision_trace`
3. LLM/graph 없이도 동작하는 deterministic link check를 먼저 강화한다.

### Do not adopt now

- `neo4j-agent-memory`를 기본 requirements에 추가하지 않는다.
- `create-context-graph` scaffold 결과물을 이 repo에 직접 vendoring하지 않는다.
- 한국어 사내 자료를 GLiNER extraction에 바로 맡기지 않는다.
- raw private documents를 NAMS 또는 cloud agent memory에 넣지 않는다.

### Future pilot gate

다음 조건이 모두 만족될 때만 Neo4j pilot을 진행한다.

1. Docker Desktop, Neo4j Desktop, Aura 중 하나가 준비되어 있다.
2. 민감 자료를 제외한 anonymized sample 3개가 있다.
   - UX screen 3개
   - packet field 3개
   - defect case 5개
3. 다음 질문에 deterministic baseline보다 빠르고 정확히 답한다.
   - "이 defect가 어떤 UX data와 packet field에 연결되는가?"
   - "이 packet scale 변경이 어떤 LCD screen과 defect memory를 건드리는가?"
   - "이 UART signal anomaly 후보의 source contract와 phase rule은 무엇인가?"
4. 설치와 재현 시간이 1시간 이내다.
5. graph 결과가 file path, YAML key, defect id, UART timestamp 중 하나로 되돌아온다.

## 최종 판정

Context graph는 이 devkit의 방향과 맞는다. 그러나 현재 이로움은 "Neo4j를 지금 설치해서 agent memory를 붙이는 것"이 아니라 "관계와 decision trace를 기존 YAML/Markdown workflow에 먼저 심는 것"이다.

따라서 다음 implementation은 graph DB 통합이 아니라, review bundle과 defect memory에 provenance path와 decision trace를 추가하는 가벼운 change가 되어야 한다.
