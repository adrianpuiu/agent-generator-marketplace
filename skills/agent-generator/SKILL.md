---
name: agent-generator
description: Generate production-ready LangGraph agents from natural language specifications. Use when users request agent creation with tool definitions, memory persistence, and reasoning loops. Supports dynamic tool binding, Redis memory backends, and executable Python scripts ready for deployment.
---

# Agent Generator Skill

Generate fully functional, production-ready LangGraph agents from natural language descriptions. This skill produces self-contained Python scripts with tool definitions, memory integration, error handling, and deployment readiness.

## Core Workflow

The generation pipeline follows a deterministic sequence:

1. **Parse requirements** from natural language description
2. **Map tools** to predefined integrations (Tavily, Polygon, Finnhub, etc.)
3. **Generate schemas** using Pydantic v2 for all tool inputs
4. **Render script** from Jinja2 template with all configurations
5. **Validate output** via AST security checks
6. **Extract dependencies** from actual imports for requirements.txt

## Inputs

When requesting agent generation, provide:

- **description**: Natural language goal ("stock sentiment agent", "multi-stock analyzer", etc.)
- **tools** (optional): Specific tool names to include. If omitted, tools are inferred from description
- **memory_backend** (optional): `redis` (persistent, agent-scoped), `postgres`, or default in-memory
- **model** (optional): Defaults to `claude-sonnet-4-20250514`

Example request:
```
Create a DeepAgent that:
1. Analyzes stock sentiment from news
2. Fetches real-time prices from Polygon.io
3. Triggers alerts when sentiment drops below -0.3
4. Maintains conversation history via Redis
```

## Output Structure

The generated agent includes:

```
generated_agent.py (executable script with):
  - Imports (langchain, langgraph, pydantic, etc.)
  - Pydantic input schemas for each tool
  - @tool decorated functions with full docstrings
  - Memory initialization (Redis/Postgres/InMemory)
  - Agent compilation with LangGraph
  - Error handling and logging
  - Main execution loop with CLI args

requirements.txt (auto-extracted from code)

setup_instructions (environment variables, API keys, etc.)
```

## Design Decisions

**LangGraph over legacy patterns**: Uses `create_react_agent` (standard) or `create_deep_agent` (research-heavy) instead of deprecated `AgentExecutor` patterns.

**No hardcoded secrets**: All API keys are environment variables. Generated scripts fail fast with clear errors if keys are missing.

**Checkpointer-based memory**: Uses LangGraph checkpointers for session persistence. Redis backend enables cross-process agent memory with agent-scoped TTL (3600s default for sessions, persistent for profiles).

**Tool ecosystem**: Supports Tavily Search, Serper, Polygon.io, Finnhub, Alpha Vantage, and custom REST APIs through tool definitions.

**Code quality**: Generated code is formatted with Black, validated with AST security checks (blocks eval/exec/compile), and tested for syntax errors before output.

## Tool Reference

See [references/tool_definitions.md](references/tool_definitions.md) for:
- Complete list of pre-built tools
- How to add custom tool definitions
- API key requirements for each tool

See [references/langgraph_patterns.md](references/langgraph_patterns.md) for:
- ReAct vs Deep Agent trade-offs
- Memory configuration patterns
- Tool invocation flow

See [references/redis_memory.md](references/redis_memory.md) for:
- Redis key hierarchy
- TTL strategies
- Connection pooling setup

## Security

Generated code validation enforces:
- No `eval`, `exec`, `compile`, `__import__`, `open` at module level
- Restricted imports (langchain, pydantic, typing, json, asyncio, logging only)
- AST syntax validation before output

## Limitations & Workarounds

| Constraint | Workaround |
|-----------|-----------|
| Very large agents (>500 lines) | Paginate output; user can merge multi-file agents |
| Complex multi-step workflows | Use DeepAgent with planning tool + sub-agents |
| Real-time data refresh | Add polling loop in main; use task scheduler (APScheduler) |
| Distributed deployment | Script runs locally; wrap with Docker for container deployment |

## Quick Start Example

Request:
```
Create an agent that analyzes AAPL stock using sentiment, price, and technical analysis tools.
Include Redis memory and error logging.
```

Output:
```python
#!/usr/bin/env python3
"""stock_analyzer_agent - Generated 2025-01-XX"""
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool
from pydantic import BaseModel, Field
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
import os, logging, asyncio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GetSentimentInput(BaseModel):
    symbol: str = Field(description="Stock ticker symbol")

@tool(args_schema=GetSentimentInput)
def get_sentiment(symbol: str) -> str:
    """Get market sentiment for stock from Finnhub"""
    api_key = os.getenv("FINNHUB_API_KEY")
    if not api_key:
        raise ValueError("FINNHUB_API_KEY not set")
    # Implementation
    return f"Sentiment for {symbol}: positive"

# ... additional tools ...

agent = create_react_agent(
    model="anthropic:claude-sonnet-4-20250514",
    tools=[get_sentiment, get_price, get_technical],
    prompt="You analyze stocks comprehensively..."
)

# Redis memory with agent scope
history = RedisChatMessageHistory(
    session_id=f"stock_agent:user123",
    url="redis://localhost:6379/0",
    key_prefix="agent:memory:",
    ttl=3600
)

wrapped_agent = RunnableWithMessageHistory(
    agent,
    get_session_history=lambda sid: history,
    input_messages_key="messages"
)

if __name__ == "__main__":
    result = wrapped_agent.invoke(
        {"messages": [{"role": "user", "content": "Analyze AAPL"}]},
        config={"configurable": {"session_id": "user123"}}
    )
    print(result)
```

## Implementation Scripts

See [scripts/](scripts/) for:
- `generate_agent.py` - Main generation orchestrator
- `validate_code.py` - AST security validator
- `extract_dependencies.py` - Dependency extraction
