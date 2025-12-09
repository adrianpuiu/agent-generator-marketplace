# Agent Generator Plugin for Claude Code

Transform natural language descriptions into production-ready LangGraph agents instantly.

```
You:  /generate-agent "analyze stock sentiment with Redis memory"
↓
Claude Code executes the skill
↓
You get: Python script + requirements + setup instructions
```

## Installation

```bash
# In Claude Code
/plugin marketplace add https://github.com/adrianpuiu/agent-generator-marketplace
/plugin install agent-generator
```

## Quick Start

```bash
/generate-agent "search the web and summarize results"
```

Claude Code generates:
- **generated_agent.py** - Fully executable agent script
- **requirements.txt** - Dependencies
- **setup_instructions.md** - Deployment guide

Then deploy:
```bash
pip install -r requirements.txt
python generated_agent.py "Your query"
```

## Available Commands

### /generate-agent
Generate a production-ready LangGraph agent.

```bash
/generate-agent "your description here"
/generate-agent "analyze stocks" --memory redis --deep-agent yes
```

### /list-tools
See all available tools for agent integration.

```bash
/list-tools
```

## Real Examples

### 1. Web Search Agent
```bash
/generate-agent "search for latest AI news and summarize trends"
```

### 2. Stock Analyzer
```bash
/generate-agent "track stock sentiment and alert when below -0.3" --memory redis
```

### 3. Research Agent
```bash
/generate-agent "research quantum computing and generate investment thesis" --deep-agent yes
```

## What's Generated

Each agent includes:
- ✅ Tool definitions with Pydantic schemas
- ✅ Error handling and logging
- ✅ Memory options (Redis/Postgres/In-memory)
- ✅ ReAct or DeepAgent framework
- ✅ Complete documentation
- ✅ Ready to customize and deploy

## Available Tools

**Web & Search**: Tavily, Serper  
**Finance**: Finnhub, Polygon.io, Alpha Vantage, IEX Cloud  
**Database**: Redis, PostgreSQL  
**Custom**: Any REST API  

## Features

✅ **Production-Ready** - Generated code runs immediately  
✅ **No Manual Editing** - All boilerplate included  
✅ **Security Validated** - AST-checked code  
✅ **Memory Integration** - Redis/Postgres/In-memory  
✅ **Multiple Frameworks** - ReAct or DeepAgent  
✅ **Auto Dependencies** - requirements.txt extracted  

## After Generation

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set environment variables
export FINNHUB_API_KEY="your_key"
export POLYGON_API_KEY="your_key"

# 3. Run agent
python generated_agent.py "Your query"

# 4. Customize (optional)
# Edit generated_agent.py to add real API logic
```

## Documentation

- **[SKILL.md](skills/agent-generator/SKILL.md)** - Full skill documentation
- **[generate-agent.md](commands/generate-agent.md)** - Command details
- **[list-tools.md](commands/list-tools.md)** - Available tools

## Version

- **Plugin Version**: 1.0.0
- **Python Required**: 3.10+
- **Status**: Production-Ready ✅

## License

MIT License
