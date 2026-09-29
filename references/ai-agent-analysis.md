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

For absent Agents, identify a real manual loop, available safe tools, and measurable task success. Prefer read-only tools first. Require least privilege, audit logs, prompt/data boundaries, confirmation for writes, bounded steps/cost, failure recovery, and evaluation cases. Recommend conventional automation when reasoning adds no value.
