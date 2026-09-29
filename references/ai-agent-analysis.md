# AI, LLM, and Agent analysis

Search provider SDKs and model names (OpenAI, Anthropic, Gemini, DeepSeek, Qwen, Ollama), orchestration frameworks (Spring AI, LangChain/LangChain4j, LlamaIndex, Semantic Kernel), embeddings/vector stores, prompt/config files, tool schemas, MCP transports, and workflow graphs.

Use three evidence layers: dependency, code, and runtime flow. Classify independently:

- **LLM API:** model invocation and response handling.
- **Embedding:** text/data transformed to vectors.
- **RAG:** retrieval results are intentionally supplied to generation.
- **Tool calling:** model selects structured callable tools and results return to the model or controller.
- **Workflow:** explicit deterministic or conditional orchestration; need not be Agentic.
- **Agent:** goal-directed iterative reasoning/action with tools and observations.
- **Multi-Agent:** multiple distinct agent roles exchange/delegate work; multiple model calls are insufficient.
- **MCP:** actual MCP client/server protocol implementation or configuration; ordinary function tools are insufficient.

## Opportunity decision

For an absent Agent, cite repository evidence and, separately, workflow evidence. Evaluate each gate:

1. **Real workflow:** a recurring user/operator goal and current steps are evidenced, not merely imagined.
2. **Judgment need:** inputs or next actions vary enough that fixed rules are inadequate. If rules are sufficient, recommend deterministic automation or workflow orchestration.
3. **Tool loop:** safe, observable tools can support `Goal → Reasoning → Tool → Observation → Next Action`; a chatbot alone fails this gate.
4. **Bounded value:** success and failure can be evaluated on a representative task set.
5. **Safety:** permissions, data boundaries, audit, stop conditions, and human approval make a candidate-sized MVP credible.

Select exactly one outcome:

- `PROPOSE_AGENT`: all five gates pass; document evidence and remaining risk.
- `RECOMMEND_DETERMINISTIC_AUTOMATION`: a real workflow exists but model judgment or an iterative tool loop is unnecessary.
- `NO_SUITABLE_OPPORTUNITY`: the repository offers no useful, bounded AI/automation problem.
- `INSUFFICIENT_EVIDENCE`: workflow or tool evidence is too thin to decide; list the questions/artifacts needed.

Do not treat novelty, an LLM dependency, or resume appeal as a positive signal. Prefer read-only tools first. Require least privilege, audit logs, prompt/data boundaries, confirmation for writes, bounded steps/cost, failure recovery, and evaluation cases.
