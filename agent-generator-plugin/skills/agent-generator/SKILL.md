---
name: DeepAgent Architect
description: |
  Creates production-ready DeepAgents for complex problem-solving,
  research automation, and multi-step agentic workflows.
  
  DeepAgents excel at:
  - Complex reasoning with iterative planning
  - Multi-step research and analysis
  - Coordinating teams of sub-agents
  - Adaptive problem-solving
  - Long-running analysis tasks

triggers:
  - "research"
  - "deep analysis"
  - "analyze and plan"
  - "coordinate agents"
  - "complex problem"
  - "multi-step workflow"
  - "iterative solution"
  - "market research"
  - "data analysis"
  - "root cause"
  - "investigate"
---

# DeepAgent Architect Skill

## Overview

This skill enables Claude Code to generate fully functional, production-ready DeepAgents from natural language descriptions. DeepAgents are purpose-built for complex reasoning, iterative planning, and coordinating teams of specialized agents.

## When to Use This Skill

Activate this skill with phrases like:
- "Research AI healthcare companies"
- "Analyze market trends for opportunities"
- "Coordinate a team of agents to monitor stocks"
- "Deep dive into this problem space"
- "Investigate and propose solutions"

## What DeepAgents Do Better

### Iterative Planning
- Creates step-by-step plans
- Executes with feedback loops
- Refines approach based on results
- Improves with each iteration

### Complex Reasoning
- Multi-step problem solving
- Deep analysis and synthesis
- Adaptive workflows
- Evidence-based recommendations

### Sub-Agent Coordination
- Spawn coordinated agents
- Parallel processing
- Result aggregation
- Team-based problem solving

## Generated Agent Components

### 1. Python Script (generated_agent.py)
- 600+ lines of production code
- DeepAgent framework (LangGraph)
- Built-in planning tools
- Tool definitions with Pydantic validation
- Error handling and logging
- Memory initialization (Redis/Postgres)
- Sub-agent spawning support

### 2. Planning Tools (Automatic)
Every generated agent includes:
- `create_plan()` - Generate step-by-step plans
- `refine_plan()` - Improve plans based on feedback
- `decompose_task()` - Break complex tasks into steps
- `evaluate_solution()` - Rate solutions against criteria

### 3. Dependencies (requirements.txt)
```
langgraph>=0.1.0
langchain>=0.3.0
pydantic>=2.0.0
redis>=5.0.0
```

## Example Use Cases

### Research Agent
```
User: "Research emerging AI healthcare companies"

Generated agent:
1. Plans research approach
2. Searches for companies
3. Gathers funding data
4. Analyzes technology
5. Generates thesis
6. Refines findings
```

### Multi-Agent Team
```
User: "Monitor 100 stocks for patterns"

Generated:
- Coordinator (plans, delegates)
- 10 Worker Sub-Agents (parallel analysis)
- Alert Agent (anomalies)
- Reporter (summary)
```

### Problem Solver
```
User: "How to optimize our pipeline?"

Generated agent:
1. Analyzes current state
2. Identifies bottlenecks
3. Generates solutions
4. Evaluates each
5. Refines recommendations
```

## Key Features

✅ **Iterative Planning** - Multi-step with refinement  
✅ **Planning Tools** - Built-in planning capability  
✅ **Sub-Agents** - Spawn and coordinate  
✅ **Long-Running** - Research and analysis tasks  
✅ **Memory-Aware** - Stores intermediate results  
✅ **Production-Ready** - Fully functional immediately  

## Next Steps

1. Install dependencies: `pip install -r requirements.txt`
2. Configure environment: `export FINNHUB_API_KEY=...`
3. Run agent: `python generated_agent.py "your query"`

---

**Create DeepAgents now**: Tell Claude Code what to research or analyze!

---

## Specialized Commands (Phase 2)

Beyond the generic `/generate-agent`, use these specialized commands for common use cases:

### Research Agent
```
/research-agent "topic"
```
Pre-configured for web research with search tools, web scraping, and iterative analysis refinement.

**Best for:** Market research, competitive analysis, investment due diligence, trend analysis

**Includes:** Web search tools, analysis framework, source evaluation, iterative refinement

### Analysis Agent
```
/analysis-agent "analysis goal"
```
Pre-configured for data analysis with statistical tools, pattern detection, and visualization.

**Best for:** Data exploration, pattern detection, trend analysis, anomaly detection, forecasting

**Includes:** Data loading, pattern detection, statistical analysis, visualization tools

### Problem Solver
```
/problem-solver "problem statement"
```
Pre-configured for systematic problem-solving with root cause analysis and solution generation.

**Best for:** Root cause analysis, optimization, process improvement, debugging, strategy

**Includes:** Problem decomposition, root cause investigation, solution generation, evaluation

### Multi-Agent Team
```
/multi-agent-team "task" --num-agents 10
```
Creates a coordinated team of parallel agents for large-scale analysis.

**Best for:** Processing 100+ items, parallel analysis, portfolio monitoring, batch processing

**Includes:** Coordinator, N worker agents, aggregator, reporter

## When to Use Each

| Situation | Command | Why |
|-----------|---------|-----|
| Research a topic | `/research-agent` | Web search optimized |
| Explore data | `/analysis-agent` | Data tools built-in |
| Fix a problem | `/problem-solver` | RCA tools included |
| Analyze 100+ items | `/multi-agent-team` | Parallel processing |
| Custom workflow | `/generate-agent` | Full customization |

---
