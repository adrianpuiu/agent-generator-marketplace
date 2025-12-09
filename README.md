# Agent Generator Plugin for Claude Code

Transform natural language descriptions into production-ready LangGraph agents instantly through Claude Code.

```
You: /generate-agent "analyze stock sentiment with Redis memory"
↓
Claude Code executes the skill
↓
You get: Python script + requirements + setup instructions
```

## Installation

### Quick Install

```bash
# From Claude Code
/plugin install agent-generator
```

### Install from Marketplace

```bash
# Add the plugin marketplace
/plugin marketplace add https://github.com/adrianpuiu/agent-generator-marketplace

# Install the plugin
/plugin install agent-generator@your-marketplace
```

### Verify Installation

```bash
/help
# You should see:
# /generate-agent - Generate a production-ready LangGraph agent
# /list-tools - List available tools for agents
```

## Usage

### Basic: Generate a Simple Agent

```bash
/generate-agent "search the web and summarize results"
```

### With Options: Stock Analyzer

```bash
/generate-agent "analyze stock sentiment and price movements" \
  --tools sentiment,price \
  --memory redis
```

### Complex: Research Agent

```bash
/generate-agent "research AI trends, analyze impact, generate investment thesis" \
  --deep-agent yes
```

## What You Get

When you run `/generate-agent`, Claude Code generates three files:

### 1. `generated_agent.py` (executable script)
```python
#!/usr/bin/env python3
# Complete, production-ready agent with:
# - Tool definitions with Pydantic schemas
# - Error handling and logging
# - Memory initialization (Redis/Postgres/In-memory)
# - Agent setup (ReAct or DeepAgent)
# - Main execution loop
# - CLI support
```

### 2. `requirements.txt` (dependencies)
```
langgraph>=0.1.0
langchain>=0.3.0
langchain-core>=0.3.0
pydantic>=2.0.0
redis>=5.0.0
```

### 3. `setup_instructions.md` (deployment guide)
```
# Setup Instructions

## Environment Variables
export FINNHUB_API_KEY="xxx"
export POLYGON_API_KEY="xxx"
export REDIS_URL="redis://localhost:6379/0"

## Run Agent
pip install -r requirements.txt
python generated_agent.py "Your query"
```

## Examples

### Example 1: Simple Web Search Agent
```bash
/generate-agent "search for latest AI news and summarize trends"
```
**Output**: Agent that searches web and provides summaries

### Example 2: Financial Portfolio Agent
```bash
/generate-agent "track stock portfolio with sentiment, price, and technical analysis. Alert when sentiment drops below -0.3" \
  --memory redis
```
**Output**: Agent with:
- Tool: Get sentiment from Finnhub
- Tool: Get price from Polygon.io
- Tool: Get technicals from Alpha Vantage
- Memory: Redis for persistence
- Alerts: Automated on conditions

### Example 3: Deep Research Agent
```bash
/generate-agent "research quantum computing trends, analyze impact on tech stocks, generate investment recommendations" \
  --deep-agent yes
```
**Output**: DeepAgent with:
- Planning capability
- Multi-step research
- Sub-agent delegation
- Comprehensive analysis

## Available Tools

### Web & Search
- **Tavily Search** - Web search with structured output
- **Serper** - Google search

### Finance
- **Finnhub** - Stock sentiment, news
- **Polygon.io** - Real-time prices
- **Alpha Vantage** - Technical indicators
- **IEX Cloud** - Company fundamentals

### Database
- **Redis** - Session memory, caching
- **PostgreSQL** - Persistent storage

### Custom
- Any REST API with authentication

List all available tools:
```bash
/list-tools
```

## Customization

### Implement Tool Logic

Edit `generated_agent.py`:

```python
# Before (placeholder)
@tool
def get_sentiment(symbol: str) -> str:
    return "Result from get_sentiment"

# After (implemented)
@tool
def get_sentiment(symbol: str) -> str:
    api_key = os.getenv("FINNHUB_API_KEY")
    response = requests.get(
        "https://finnhub.io/api/v1/news-sentiment",
        params={"symbol": symbol, "token": api_key}
    )
    return f"Sentiment: {response.json().get('companyNewsScore')}"
```

### Add Custom Tools

```python
from pydantic import BaseModel, Field
from langchain_core.tools import tool

class MyToolInput(BaseModel):
    param: str = Field(description="Parameter")

@tool(args_schema=MyToolInput)
def my_tool(param: str) -> str:
    """Do something with the parameter."""
    return f"Result: {param}"
```

### Configure System Prompt

Edit the agent initialization:

```python
agent = create_react_agent(
    model="anthropic:claude-sonnet-4-20250514",
    tools=tools,
    prompt="Your custom system prompt here"
)
```

## Deployment

### Local Development
```bash
python generated_agent.py "test query"
```

### Docker Container
```dockerfile
FROM python:3.10
COPY generated_agent.py requirements.txt ./
RUN pip install -r requirements.txt
CMD ["python", "generated_agent.py"]
```

### AWS Lambda
```python
def handler(event, context):
    result = asyncio.run(run_agent(event['query']))
    return json.dumps(result)
```

### Kubernetes
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: agent
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: agent
        image: agent:latest
```

## Settings & Configuration

### In Claude Code Settings

Add to your project's `.claude/settings.json`:

```json
{
  "plugins": {
    "agent-generator": {
      "enabled": true,
      "settings": {
        "defaultMemoryBackend": "redis",
        "defaultModel": "anthropic:claude-sonnet-4-20250514",
        "pythonPath": "/usr/bin/python3"
      }
    }
  }
}
```

## Troubleshooting

### "Command not found"
```bash
# Check plugin is installed
/plugin
# You should see "agent-generator" listed

# Reinstall if needed
/plugin uninstall agent-generator
/plugin install agent-generator
```

### Generated script won't run
```bash
# Check Python version (need 3.10+)
python3 --version

# Install dependencies
pip install -r requirements.txt

# Test syntax
python3 -m py_compile generated_agent.py

# Set environment variables
export FINNHUB_API_KEY="xxx"

# Run with logging
LOG_LEVEL=DEBUG python generated_agent.py
```

### Missing API keys
```bash
# Create .env file
cat > .env << 'EOF'
FINNHUB_API_KEY=xxx
POLYGON_API_KEY=xxx
REDIS_URL=redis://localhost:6379/0
EOF

# Load environment
source .env
```

## Features

✅ **Instant Generation** - Natural language → production code  
✅ **No Manual Editing** - Script runs immediately  
✅ **Security Validated** - AST checks, no dangerous patterns  
✅ **Memory Integration** - Redis/Postgres/In-memory options  
✅ **Multiple Frameworks** - ReAct or DeepAgent  
✅ **Auto Dependencies** - requirements.txt extracted automatically  
✅ **Error Handling** - Comprehensive try/except blocks  
✅ **Logging** - Full debugging and monitoring  
✅ **Customizable** - Edit and extend as needed  

## What's Included

- **Embedded Skill** - Agent-generator-skill built into the plugin
- **Commands** - `/generate-agent`, `/list-tools`
- **Documentation** - Complete guides and examples
- **Scripts** - Generation engine and validators
- **Examples** - Reference agent outputs

## Workflow

```
1. Ask Claude: /generate-agent "your description"
2. Claude generates: agent.py + requirements.txt + setup
3. Install: pip install -r requirements.txt
4. Configure: Set environment variables
5. Deploy: python agent.py "query"
6. Customize: Edit tool implementations
7. Scale: Docker/Lambda/Kubernetes
```

## Documentation

- **[SKILL.md](skills/agent-generator/SKILL.md)** - Core skill documentation
- **[generate-agent.md](commands/generate-agent.md)** - Command details
- **[list-tools.md](commands/list-tools.md)** - Available tools

## Version

- **Plugin Version**: 1.0.0
- **Skill Version**: 1.0.0
- **Python Required**: 3.10+
- **Status**: Production-Ready ✅

## Support

For issues or questions:

1. Check the troubleshooting section above
2. Review command documentation: `/help generate-agent`
3. List available tools: `/list-tools`
4. Check generated agent's docstrings

## Contributing

Contributions welcome! Please ensure:
- Code follows existing patterns
- Generated agents remain production-ready
- Security validation passes
- Documentation is updated

## License

MIT License - See LICENSE.md

---

**Get started now**: `/generate-agent "what you want your agent to do"` 🚀
