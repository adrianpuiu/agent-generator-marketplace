# DeepAgent Architect Plugin for Claude Code

Generate production-ready DeepAgents with built-in planning for complex reasoning, research automation, and multi-step problem-solving.

```
You:  /generate-agent "research emerging AI healthcare companies"
↓
Claude Code creates DeepAgent with planning
↓
You get: Python script + planning tools + memory + setup guide
```

## Installation

```bash
# In Claude Code
/plugin marketplace add https://github.com/adrianpuiu/agent-generator-marketplace
/plugin install agent-generator
```

## What is a DeepAgent?

DeepAgents are optimized for **complex, multi-step tasks** that require:
- ✅ Planning and strategy
- ✅ Iterative refinement
- ✅ Complex reasoning
- ✅ Research automation
- ✅ Coordinated sub-agents

Not for simple tasks - they're planning-first, reasoning-heavy agents.

## Quick Start

```bash
/generate-agent "research quantum computing companies and analyze funding"
```

Claude Code generates:
- **generated_agent.py** - Complete DeepAgent (600+ lines)
- **requirements.txt** - Dependencies  
- **setup_instructions.md** - Deployment guide

## What's Included

### Built-In Planning Tools (Automatic)
Every agent includes:
```python
create_plan()        # Plan the approach
decompose_task()     # Break into steps
evaluate_solution()  # Rate solutions
refine_plan()        # Improve iteratively
```

### Framework
- LangGraph DeepAgent (optimized for planning)
- Async execution for long-running tasks
- Memory persistence (Redis/Postgres)
- Full error handling and logging

### Example Generated Code
```python
agent = create_deep_agent(
    model="claude-sonnet-4-20250514",
    tools=[user_tools + planning_tools],
    max_iterations=15,
)

# Automatically:
# 1. Plans approach
# 2. Decomposes task
# 3. Executes with tools
# 4. Evaluates results
# 5. Refines based on feedback
```

## Commands

### Generate Agent
```
/generate-agent "description"
/generate-agent "description" --memory redis
```

Options:
- `--memory` - `memory` (default), `redis`, or `postgres`

### List Tools
```
/list-planning-tools
```

Shows planning tools and available integrations.

## Examples

### Example 1: Research (Multi-Step)
```
/generate-agent "Research AI healthcare companies - identify funding, technology, and competitive advantages"
```

Agent automatically:
1. Plans research strategy
2. Searches for companies
3. Gathers funding data
4. Analyzes technology
5. Evaluates competitiveness
6. Refines thesis iteratively

### Example 2: Analysis with Evaluation
```
/generate-agent "Analyze 50 stocks for unusual patterns and rank top 5"
```

Agent:
1. Plans analysis approach
2. Decomposes stock analysis
3. Runs pattern detection
4. Evaluates against criteria
5. Ranks results
6. Refines rankings

### Example 3: Problem Solving
```
/generate-agent "Identify system bottlenecks and propose optimization solutions"
```

Agent:
1. Plans analysis approach
2. Analyzes system
3. Decomposes problem
4. Generates solutions
5. Evaluates each solution
6. Refines recommendations

## Key Features

### Planning-First Architecture
- Every agent plans before acting
- Built-in decomposition
- Solution evaluation
- Iterative refinement

### Complex Reasoning
- Multi-step workflows
- Adaptive problem solving
- Feedback loops
- Evidence-based decisions

### Production-Ready
- 600+ lines of generated code
- Complete error handling
- Comprehensive logging
- API key management
- Ready to deploy

### Memory Options
- **Default**: In-process (dev)
- **Redis**: Distributed (production)
- **Postgres**: Persistent (archives)

## After Generation

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure environment
export FINNHUB_API_KEY="..."
export REDIS_URL="redis://localhost:6379/0"

# 3. Run agent
python generated_agent.py "your query"
```

## Customization

Generated agents are fully customizable:
- Implement tool logic with real API calls
- Adjust planning prompts
- Add domain-specific tools
- Integrate with your systems
- Add custom evaluation criteria

## Use Cases

- **Research Automation** - Deep investigation with planning
- **Market Analysis** - Stock/crypto analysis with strategy
- **Problem Solving** - Root cause analysis and recommendations
- **Data Analysis** - Complex multi-step data exploration
- **Coordinated Work** - Teams of sub-agents in parallel

## Requirements

- Python 3.10+
- Claude Sonnet model
- LangGraph + LangChain
- Optional: Redis or PostgreSQL

## Deployment

Generated agents can deploy to:
- Local machine
- Docker container
- AWS Lambda
- Kubernetes
- Systemd service
- Cloud Functions

See `setup_instructions.md` in generated output.

---

**Start now**: `/generate-agent "what you want to research or analyze"`

Built with ❤️ for complex, reasoning-heavy tasks.
