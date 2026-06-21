# 01. Evidence Map

이 문서는 AX 계획에 사용한 공개 근거를 정리한다. 실제 사내 자료와 회사명은 포함하지 않는다.

## Design-to-Agent

공식 디자인 도구 MCP 문서는 디자인 파일의 정보와 문맥을 AI agent가 코드 생성에 사용할 수 있게 제공한다고 설명한다. 또한 frame 선택 기반 code generation, variables/components/layout data 추출, design system context 사용이 가능하다고 설명한다.

- Source: https://developers.figma.com/docs/figma-mcp-server/
- 적용: UX 화면을 직접 코드로 생성하기보다, 제품개발자에게 필요한 `screen -> required data -> packet field` 추출에 사용한다.

## Document Parsing For GenAI

Docling은 PDF/DOCX/PPTX/XLSX/HTML 등 다양한 형식을 parsing하고, PDF layout, reading order, table structure, OCR, Markdown/JSON export, local execution, air-gapped 환경을 지원한다고 밝힌다.

- Source: https://github.com/docling-project/docling
- 적용: UX PDF, 사양 PDF를 Markdown/JSON으로 변환하고 내부 wiki/RAG에 넣는다.

## File Search / RAG

OpenAI File Search는 vector store에 업로드한 파일을 semantic/keyword search로 검색해 응답 전 관련 정보를 검색하게 하는 hosted tool이다.

- Source: https://developers.openai.com/api/docs/guides/tools-file-search
- 적용: 민감도가 낮거나 외부 사용이 허용된 문서만 cloud RAG에 넣고, 사내 자료는 local RAG 우선으로 둔다.

## Agent Operating Instructions

Codex는 `AGENTS.md`를 작업 전 읽고, global/project/directory scope의 guidance를 instruction chain으로 구성한다.

- Source: https://developers.openai.com/codex/guides/agents-md
- 적용: 리팩토링 agent가 scheduler, packet, 사양 근거 없이 코드를 바꾸지 않도록 repo-level contract를 둔다.

## Effective Agents

Anthropic은 성공적인 agent 구현이 복잡한 framework보다 단순하고 조합 가능한 pattern을 사용했다고 정리한다.

- Source: https://www.anthropic.com/engineering/building-effective-agents
- 적용: 처음부터 완전 autonomous agent를 만들지 않고, ingest -> contract -> review bundle -> deterministic check 순서의 workflow를 만든다.

## Agent Evals

Anthropic은 eval이 agent 문제와 행동 변화를 production 전에 드러내며, automated eval은 input과 grading logic으로 output success를 측정한다고 설명한다. OpenAI도 trace, grader, dataset, eval run으로 agent workflow 품질을 개선하라고 설명한다.

- Sources:
  - https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
  - https://developers.openai.com/api/docs/guides/agent-evals
- 적용: 결함 이력을 AI prompt 개선용 anecdote가 아니라 repeatable eval dataset으로 바꾼다.

## AI Code Review Rules

AI code review 도구들은 `AGENTS.md`, `CLAUDE.md`, `.github/copilot-instructions.md`, `.rules/*` 같은 guideline 파일을 review criteria로 사용할 수 있고, project-specific context와 business logic validation도 제공한다.

- Sources:
  - https://docs.coderabbit.ai/knowledge-base/code-guidelines
  - https://docs.kodus.io/knowledge_base/en/introduction
- 적용: packet/scheduler/UX contract를 review criteria로 사용한다.

## Excel Requirement Ingest

pandas `read_excel`은 `xls`, `xlsx`, `xlsm`, `xlsb`, `odf`, `ods`, `odt`를 local filesystem 또는 URL에서 읽고 sheet 단위 읽기를 지원한다.

- Source: https://pandas.pydata.org/docs/reference/api/pandas.read_excel.html
- 적용: MRT/SRT/과제 사양 Excel을 JSONL/Markdown chunks로 변환한다.

## PDF / Table / OCR

Azure Document Intelligence layout model은 PDF와 image 등에서 OCR, text, tables, selection marks, document structure를 추출할 수 있다고 설명한다. AWS Textract도 scanned documents, PDFs, images, tables, forms에서 text/handwriting/layout/data 추출을 제공한다.

- Sources:
  - https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/prebuilt/layout
  - https://aws.amazon.com/textract/
- 적용: Docling으로 안 되는 복잡한 표/스캔본은 cloud OCR 후보로 분리한다.

## UART / Quality Time Series

tsfresh는 time series characteristics를 자동 계산하고 classification/regression에 유용한 feature 평가 기능을 제공한다. ruptures는 non-stationary signal의 offline change point detection을 제공한다. PyOD는 tabular, time series 등 다양한 데이터의 anomaly detection API를 제공한다.

- Sources:
  - https://tsfresh.readthedocs.io/
  - https://github.com/deepcharles/ruptures
  - https://github.com/yzhao062/pyod
- 적용: 200 ms UART 로그에서 phase transition, 급수 종료, 모터 회전 profile, 이상구간 후보를 자동 표시한다.

## Local Coding Model

Ollama의 Qwen2.5-Coder page는 7B 모델이 약 4.7 GB, 32K context window를 가진다고 표시한다. Qwen3-Coder는 agentic coding과 local development를 목표로 하는 code model 계열이라고 설명한다.

- Sources:
  - https://ollama.com/library/qwen2.5-coder
  - https://github.com/QwenLM/Qwen3-Coder
- 적용: GTX 3050 Ti 환경에서는 7B급 모델을 기본으로 두고, 큰 리팩토링은 cloud coding agent 예산을 사용한다.

