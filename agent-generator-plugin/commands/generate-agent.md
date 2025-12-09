---
description: Generate a production-ready DeepAgent from natural language specification
argument-hint: "[description]"
---

# Generate DeepAgent

Generate a complete, production-ready DeepAgent from a natural language description.

DeepAgents are designed for **complex reasoning, iterative planning, and research automation**.

## Usage

```
/generate-agent "identify emerging quantum computing startups and analyze funding"
```

With options:

```
/generate-agent "analyze market trends" --memory redis
/generate-agent "multi-company analysis" --spawn-sub-agents yes
```

## What You Get

1. **generated_agent.py** - Fully executable Python script (600+ lines)
2. **requirements.txt** - All dependencies auto-extracted
3. **setup_instructions.md** - Environment setup and deployment guide

## Output includes:
- ✅ **Built-in Planning Tools** - create_plan, refine_plan, decompose_task, evaluate_solution
- ✅ **Iterative Reasoning** - Multi-step problem solving with planning
- ✅ **Tool definitions** with Pydantic schemas
- ✅ **Error handling** and comprehensive logging
- ✅ **Redis/Postgres Memory** - Persistent research sessions
- ✅ **Sub-agent Support** - Coordinate teams of agents
- ✅ **LangGraph DeepAgent Framework** - Production-ready

## Real Examples

### Research Agent (Web Search + Analysis)
```
/generate-agent "What are the top AI healthcare companies? Analyze their technology, funding, and competitive advantages."
```
Generates agent that:
1. Plans research approach
2. Searches for companies
3. Gathers funding/technology data
4. Analyzes competitiveness
5. Generates investment thesis
6. Iteratively refines findings

### Multi-Agent Team (Parallel Analysis)
```
/generate-agent "Monitor 100 stocks for unusual trading patterns" --spawn-sub-agents yes
```
Generates:
- Coordinator Agent (plans work, delegates)
- 10 Pattern Detector Sub-Agents (parallel analysis)
- Alert Agent (flags anomalies)
- Reporter Agent (generates summary)

### Problem Solver (Root Cause + Solutions)
```
/generate-agent "How can we reduce API latency? Analyze current bottlenecks and propose solutions."
```
Generates agent that:
1. Analyzes current pipeline
2. Identifies bottlenecks (with planning)
3. Generates multiple solutions
4. Evaluates each solution
5. Refines recommendations iteratively

## After Generation

```bash
pip install -r requirements.txt
export FINNHUB_API_KEY="your_key"
python generated_agent.py "Your research query"
```

## DeepAgent Features

- **Iterative Planning** - Multi-step reasoning with refinement
- **Complex Analysis** - Research automation and problem-solving
- **Sub-Agent Coordination** - Spawn teams of specialized agents
- **Planning Tools** - Built-in tools for planning and evaluation
- **Long-Running** - Ideal for research and analysis tasks
- **Adaptive** - Adjusts approach based on findings
- **Memory-Aware** - Stores intermediate plans and results
