---
description: List all available tools for agent generation
---

# List Tools

Show available tools that can be integrated into generated agents.

## Available Tools

### Web & Search
- **Tavily Search** - Web search with structured output
- **Serper** - Google search integration

### Finance
- **Finnhub** - Stock sentiment, news impact
- **Polygon.io** - Real-time prices, OHLCV
- **Alpha Vantage** - Technical indicators
- **IEX Cloud** - Company fundamentals

### Database & Storage
- **Redis** - Session memory, caching
- **PostgreSQL** - Persistent data storage

### Custom
- Any REST API with authentication

## Usage

When generating an agent, specify tools:

```
/generate-agent "your description" --tools sentiment,price,technical
```

## Tool Details

Each tool is pre-configured with:
- API key environment variables
- Rate limiting and error handling
- Request/response schemas
- Example implementations

See the generated agent's source for specific tool usage patterns.
