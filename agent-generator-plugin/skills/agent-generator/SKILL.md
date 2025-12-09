---
name: Agent Generator
description: |
  Generates production-ready LangGraph agents from natural language descriptions.
  Use when you need to create AI agents for specific tasks like data analysis,
  web search, financial analysis, or any custom automation workflow.
triggers:
  - "create an agent"
  - "generate an agent"
  - "build an agent"
  - "agent that"
  - "write an agent"
  - "agent for"
---

# Agent Generator Skill

## Overview

This skill enables Claude Code to generate fully functional, production-ready AI agents from natural language descriptions. The generated agents include all necessary components: tool definitions, error handling, logging, memory persistence, and deployment instructions.

## When to Use This Skill

- **Creating AI Agents** - "Create an agent that analyzes stock sentiment"
- **Automation Workflows** - "Build an agent that monitors and alerts"
- **Data Processing** - "Generate an agent that processes and analyzes data"
- **Research Tasks** - "Create a research agent that analyzes trends"
- **Custom Tools** - "Build an agent with custom API integrations"

Trigger this skill with phrases like:
- "create an agent"
- "generate an agent"  
- "build an agent"
- "write an agent"
- "agent for [task]"

## How It Works

1. **Parse Request** - Understand what the agent should do
2. **Generate Code** - Create complete Python script with:
   - Tool definitions
   - Pydantic schemas
   - Error handling
   - Logging
   - Memory integration
3. **Extract Dependencies** - Auto-generate requirements.txt
4. **Validate Security** - AST checks for dangerous patterns
5. **Provide Setup** - Return deployment instructions

## Features

✅ **Production-Ready** - Generated code runs immediately  
✅ **No Manual Editing** - All boilerplate included  
✅ **Security Validated** - AST-checked, no dangerous patterns  
✅ **Multiple Frameworks** - ReAct (simple) or DeepAgent (complex)  
✅ **Memory Options** - Redis, Postgres, or in-memory  
✅ **Tool Integration** - 20+ pre-built tools available  
✅ **Full Documentation** - Setup and deployment guides  

## Generated Agent Components

### 1. Python Script (generated_agent.py)
```python
#!/usr/bin/env python3
# 500+ lines of production code including:
# - Tool definitions with Pydantic validation
# - Error handling and logging
# - Memory initialization
# - Agent framework setup
# - Main execution loop
```

### 2. Dependencies (requirements.txt)
```
langgraph>=0.1.0
langchain>=0.3.0
langchain-core>=0.3.0
pydantic>=2.0.0
redis>=5.0.0  # if memory=redis
```

### 3. Setup Instructions (setup_instructions.md)
- Environment variable configuration
- API key setup
- Deployment options
- Troubleshooting guide

## Example Usage

### Simple Web Search Agent
```
/generate-agent "search the web and summarize results"
```

### Stock Analysis Agent
```
/generate-agent "analyze stock sentiment and price movements" \
  --memory redis \
  --tools sentiment,price
```

### Research Agent with Planning
```
/generate-agent "research quantum computing trends and generate report" \
  --deep-agent yes
```

## Next Steps After Generation

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment**
   ```bash
   export FINNHUB_API_KEY="your_key"
   export POLYGON_API_KEY="your_key"
   ```

3. **Test Locally**
   ```bash
   python generated_agent.py "your query"
   ```

4. **Customize** (optional)
   - Implement tool logic with real API calls
   - Adjust system prompts
   - Add monitoring

5. **Deploy**
   - Docker: `docker build -t agent:latest .`
   - Lambda: Wrap with handler function
   - Kubernetes: Create deployment manifest

## Available Tools

The skill can generate agents with any of these tools:

**Web & Search**: Tavily Search, Serper  
**Finance**: Finnhub, Polygon.io, Alpha Vantage, IEX Cloud  
**Database**: Redis, PostgreSQL  
**Custom**: Any REST API  

Use `/list-tools` in Claude Code to see all available tools.

## Memory Backends

- **memory** - In-process (default, no external dependencies)
- **redis** - Distributed memory with TTL
- **postgres** - Enterprise-grade persistent storage

## Framework Options

- **ReAct** - Simple agents with tool calling
- **DeepAgent** - Complex tasks with planning and sub-agents

## Security

All generated agents include:
- ✅ Input validation with Pydantic
- ✅ Error handling on all API calls
- ✅ Secrets via environment variables (never hardcoded)
- ✅ Logging for debugging and monitoring
- ✅ Rate limiting and timeout handling

## Customization

Generated agents are fully customizable:

1. **Implement Tool Logic** - Replace placeholder implementations
2. **Add Custom Tools** - Create new @tool decorated functions
3. **Adjust System Prompt** - Modify agent behavior
4. **Integrate with Your Systems** - Connect to databases, APIs, services
5. **Add Monitoring** - Prometheus, CloudWatch, Datadog integration

## Deployment Options

| Option | Best For | Command |
|--------|----------|---------|
| Local | Development | `python agent.py` |
| Docker | Isolated environments | `docker run agent:latest` |
| Lambda | Serverless/event-driven | AWS Lambda handler |
| Kubernetes | Scalable services | `kubectl apply -f deployment.yaml` |
| Systemd | Long-running services | `systemctl start agent` |

## Troubleshooting

**Script won't run**
- Check Python 3.10+: `python3 --version`
- Install dependencies: `pip install -r requirements.txt`
- Set environment variables: `export FINNHUB_API_KEY=...`

**Missing tools**
- Provide detailed description: `/generate-agent "detailed description of what you need"`
- Use `/list-tools` to see available tools

**Deployment issues**
- Check setup_instructions.md for your platform
- Verify API keys are set correctly
- Review agent logs for errors

## Learning Resources

1. **Command Reference** - `/help generate-agent`
2. **Tool Listing** - `/list-tools`
3. **Generated Code** - Check docstrings in generated_agent.py
4. **Setup Guide** - See generated setup_instructions.md

## Advanced Features

### Multi-User Support
Generated agents can maintain separate conversation history per user with Redis memory.

### Alert Triggers
Create conditions-based alerts in tool implementations.

### Sub-Agents (DeepAgent)
Spawn specialized sub-agents for complex tasks.

### Custom Workflows
Chain multiple tools in custom execution patterns.

### Monitoring & Observability
Integrate with monitoring systems for production tracking.

---

**Start generating agents now**: `/generate-agent "what you want your agent to do"`
