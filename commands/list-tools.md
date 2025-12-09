---
description: List available tools for agent generation
---

# List Tools

Show all available tools that can be integrated into generated agents.

## Available Tools

### Web Search
- **Tavily Search** - General web search with structured output
- **Serper** - Google search integration
- Ideal for: News, research, information gathering

### Stock Market
- **Finnhub** - Stock sentiment, news impact
- **Polygon.io** - Real-time prices, OHLCV data
- **Alpha Vantage** - Technical indicators (SMA, RSI, MACD, BBANDS)
- **IEX Cloud** - Company fundamentals, earnings, dividends
- Ideal for: Financial analysis, portfolio tracking, alerts

### Database
- **Redis** - Session memory, caching
- **PostgreSQL** - Persistent storage, audit trails
- Ideal for: Memory persistence, scaling to multiple users

### Custom
- **REST APIs** - Any HTTP endpoint with authentication
- Ideal for: Company APIs, proprietary services

## Usage

To use specific tools in your agent:

```
/generate-agent "analyze AAPL sentiment" --tools sentiment,price
```

## Tool Details

For detailed information about each tool:
- API key requirements
- Setup instructions  
- Rate limits
- Example code

See the agent-generator-skill documentation or ask Claude for specifics.

## Need a Custom Tool?

After generating your agent, you can add custom tools by editing the `@tool` decorators in the generated Python script. Each tool needs:

1. **Function definition** with type hints
2. **Pydantic input schema** for validation
3. **Docstring** describing what it does
4. **Error handling** for API failures

Example:
```python
from pydantic import BaseModel, Field
from langchain_core.tools import tool

class MyToolInput(BaseModel):
    param1: str = Field(description="Description")

@tool(args_schema=MyToolInput)
def my_tool(param1: str) -> str:
    """Tool description"""
    # Implementation
    return result
```
