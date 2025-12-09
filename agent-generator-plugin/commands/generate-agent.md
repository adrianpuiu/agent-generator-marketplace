---
description: Generate a production-ready LangGraph agent from natural language specification
argument-hint: "[description]"
---

# Generate Agent

Generate a complete, production-ready LangGraph agent from a natural language description.

## Usage

```
/generate-agent "analyze stock sentiment with Finnhub and Polygon.io APIs"
```

With options:

```
/generate-agent "track portfolio" --memory redis --deep-agent yes
```

## What You Get

1. **generated_agent.py** - Fully executable Python script (500+ lines)
2. **requirements.txt** - All dependencies auto-extracted
3. **setup_instructions.md** - Environment setup and deployment guide

## Output includes:
- ✅ Tool definitions with Pydantic schemas
- ✅ Error handling and logging
- ✅ Optional Redis/Postgres memory
- ✅ ReAct or DeepAgent framework
- ✅ Main execution loop
- ✅ Ready to deploy immediately

## Examples

### Simple Agent
```
/generate-agent "search the web and summarize results"
```

### Stock Analyzer with Redis
```
/generate-agent "analyze AAPL sentiment and trigger alerts when below -0.3" --memory redis
```

### Research Agent
```
/generate-agent "research AI trends, analyze impact, generate thesis" --deep-agent yes
```

## After Generation

```bash
pip install -r requirements.txt
export FINNHUB_API_KEY="your_key"
python generated_agent.py "Your query"
```

## Features

- **Instant Generation** - Natural language → production code
- **No Manual Editing** - Script runs immediately
- **Security Validated** - AST checks, no dangerous patterns
- **Memory Integration** - Redis/Postgres options
- **Multiple Frameworks** - ReAct (simple) or DeepAgent (research)
- **Full Error Handling** - Comprehensive try/except blocks
- **Auto Dependencies** - requirements.txt extracted automatically
