---
description: Generate a production-ready LangGraph agent from natural language specification
aliases: 
  - agent
  - create-agent
parameters:
  - name: description
    description: Natural language description of what the agent should do (e.g., "analyze stock sentiment with Redis memory")
    required: true
  - name: tools
    description: Optional comma-separated list of tools (sentiment, price, search, etc.) - auto-generated if omitted
    required: false
  - name: memory
    description: Memory backend - "memory" (default), "redis", or "postgres"
    required: false
  - name: deep-agent
    description: Use DeepAgent for complex research tasks with planning and sub-agents (yes/no)
    required: false
---

# Generate Agent

Generate a complete, production-ready LangGraph agent from a natural language description. The generated agent includes:

- ✅ Executable Python script (500+ lines)
- ✅ Tool definitions with Pydantic schemas
- ✅ Error handling and logging
- ✅ Optional Redis/Postgres memory
- ✅ Agent framework (ReAct or DeepAgent)
- ✅ requirements.txt (auto-extracted)
- ✅ Setup instructions

## Usage

```
/generate-agent "analyze stock sentiment using Finnhub and Polygon.io APIs"
```

With options:

```
/generate-agent "track portfolio performance" --tools sentiment,price --memory redis --deep-agent yes
```

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

## Output

The command will generate three files in your project:

1. **generated_agent.py** - Fully functional executable script (no editing needed)
2. **requirements.txt** - All dependencies (just `pip install -r requirements.txt`)
3. **setup_instructions.md** - Environment variables and deployment guide

Then deploy immediately:
```bash
pip install -r requirements.txt
python generated_agent.py "Your query"
```

## Features

- **No Manual Coding Required**: Generated script is production-ready
- **Security Validated**: Code passes AST security checks
- **Redis Memory**: Optional persistent agent memory with TTL
- **Multiple Frameworks**: Choose ReAct (simple) or DeepAgent (research)
- **Auto Dependencies**: requirements.txt extracted automatically
- **Full Logging**: Comprehensive error handling and debugging

## Customization

Edit `generated_agent.py` to:
1. Implement tool logic (replace placeholders)
2. Add custom system prompts
3. Integrate with your APIs
4. Deploy to Docker/Lambda/Kubernetes

## Next Steps

1. Generate agent with this command
2. Install dependencies: `pip install -r requirements.txt`
3. Set environment variables: `export FINNHUB_API_KEY=...`
4. Test: `python generated_agent.py "test query"`
5. Deploy with Docker/Kubernetes as needed
