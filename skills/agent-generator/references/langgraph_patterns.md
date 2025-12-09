# LangGraph Patterns for Agent Generation

## ReAct vs Deep Agent

### ReAct Agent (Standard)
Use for:
- Single-step tools (web search, API calls)
- Deterministic workflows
- Agents with <10 tools
- Real-time response requirements

```python
from langgraph.prebuilt import create_react_agent

agent = create_react_agent(
    model="anthropic:claude-sonnet-4-20250514",
    tools=[get_weather, get_news, calculate],
    prompt="You are a helpful research assistant"
)

result = agent.invoke({"messages": [{"role": "user", "content": "..."}]})
```

**Flow**: User Input → Reasoning → Tool Call → Tool Result → Loop Until Done

### Deep Agent (Research-Heavy)
Use for:
- Complex multi-step research tasks
- Sub-agent delegation needed
- Planning required upfront
- Long-horizon goals (>10 steps)

```python
from deepagents import create_deep_agent

agent = create_deep_agent(
    model="anthropic:claude-sonnet-4-20250514",
    tools=[search, analyze, summarize],
    system_prompt="You are a research agent with planning capabilities"
)

# Includes built-in write_todos, spawn_subagent tools
result = agent.invoke({
    "messages": [{"role": "user", "content": "Research quantum computing trends"}]
})
```

**Flow**: User Input → Plan (write_todos) → Execute (tool calls) → Delegate (spawn_subagent) → Aggregate Results

## Tool Invocation Patterns

### Synchronous (blocking)
```python
result = agent.invoke(
    {"messages": [{"role": "user", "content": "..."}]},
    config={"configurable": {"thread_id": "session_123"}}
)
print(result)
```

### Asynchronous (non-blocking)
```python
import asyncio

async def run():
    result = await agent.ainvoke(
        {"messages": [...]},
        config={"configurable": {"thread_id": "session_123"}}
    )
    return result

asyncio.run(run())
```

### Streaming (real-time output)
```python
for event in agent.stream(
    {"messages": [{"role": "user", "content": "..."}]},
    config={"configurable": {"thread_id": "session_123"}},
    stream_mode="updates"
):
    print(f"Event: {event}")
```

## Memory & Checkpointer Configuration

### In-Memory (Development)
```python
from langgraph.checkpoint.memory import InMemorySaver

checkpointer = InMemorySaver()
agent = create_react_agent(model="...", tools=[...])
app = agent.compile(checkpointer=checkpointer)

result = app.invoke(
    {"messages": [...]},
    config={"configurable": {"thread_id": "session_123"}}
)
```
- **Pros**: No external dependencies, fast, simple
- **Cons**: Memory lost on process restart, single-process only

### PostgreSQL (Production)
```python
from langgraph.checkpoint.postgres import PostgresSaver

checkpointer = PostgresSaver.from_conn_string(
    "postgresql://user:pass@localhost:5432/agent_db"
)
app = agent.compile(checkpointer=checkpointer)
```
- **Pros**: Persistent across restarts, queryable
- **Cons**: Setup required, slower than memory

### Redis (Recommended)
See [redis_memory.md](redis_memory.md) for complete Redis integration guide.

## Tool Definition Patterns

### Simple Decorator Pattern
```python
from langchain_core.tools import tool

@tool
def get_weather(city: str) -> str:
    """Get weather for a city."""
    return f"Sunny in {city}"
```
- Minimal code, automatic docstring-based description

### Structured with Pydantic
```python
from pydantic import BaseModel, Field
from langchain_core.tools import tool

class GetWeatherInput(BaseModel):
    city: str = Field(description="City name")
    unit: Literal["C", "F"] = Field(default="C", description="Temperature unit")

@tool(args_schema=GetWeatherInput)
def get_weather(city: str, unit: str = "C") -> str:
    """Get weather for a city with unit preference."""
    temp = get_temp_api(city)
    if unit == "F":
        temp = (temp * 9/5) + 32
    return f"{temp}° {unit} in {city}"
```
- Rich parameter validation, clear schema, better LLM understanding

### Custom BaseTool Subclass
```python
from langchain_core.tools import BaseTool
from typing import Optional

class CustomWeatherTool(BaseTool):
    name = "weather"
    description = "Get weather information"
    
    def _run(self, city: str) -> str:
        return get_weather_api(city)
    
    async def _arun(self, city: str) -> str:
        return await get_weather_async(city)

tool = CustomWeatherTool()
```
- Maximum control, async support, custom validation

## Error Handling Pattern

Generated agents should include:

```python
import logging
from typing import Optional

logger = logging.getLogger(__name__)

def safe_tool_call(func, *args, **kwargs) -> str:
    """Wrap tool calls with error handling."""
    try:
        return func(*args, **kwargs)
    except KeyError as e:
        logger.error(f"Missing API key: {e}")
        return f"Error: Set {str(e)} environment variable"
    except ConnectionError as e:
        logger.error(f"API unavailable: {e}")
        return "Error: Could not reach API. Retry later."
    except Exception as e:
        logger.error(f"Tool error: {type(e).__name__}: {e}")
        return f"Error: {str(e)}"
```

Then use in agent system prompt:
```
If a tool returns an error, explain the issue to the user and suggest next steps.
Do not retry failed tools without user instruction.
```

## LangChain v1.0 Migration Notes

**Deprecated (remove from generated code)**:
- `AgentExecutor`
- `initialize_agent`
- `ConversationBufferMemory`
- `ZeroShotAgent`

**Replacements (use in generated code)**:
- `create_react_agent` / `create_deep_agent`
- `LangGraph` checkpointers
- `RedisChatMessageHistory`
- Direct `@tool` decorators

Minimum Python: 3.10+
