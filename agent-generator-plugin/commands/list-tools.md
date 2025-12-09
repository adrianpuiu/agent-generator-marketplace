---
description: List planning tools and available integrations for DeepAgents
argument-hint: "[optional-category]"
---

# Planning & Integration Tools for DeepAgents

## Planning Tools (Built-In to Every Agent) 🚀

These are **automatically included** in every generated DeepAgent:

- **create_plan(goal, context)** - Generate step-by-step plans
- **refine_plan(plan, feedback)** - Iteratively improve plans
- **decompose_task(task)** - Break complex tasks into steps
- **evaluate_solution(solution, criteria)** - Rate solutions

---

## Integration Tools (Choose Based on Task)

### Web & Search
- **Tavily Search** - Web search with real-time results
- **Serper** - Search engine results with metadata

### Finance
- **Finnhub** - Stock sentiment, news, pricing
- **Polygon.io** - Real-time prices, technical data
- **Alpha Vantage** - Technical indicators, time-series
- **IEX Cloud** - Company fundamentals, analysis

### Database & Storage
- **Redis** - Session memory for long research tasks
- **PostgreSQL** - Persistent storage for analysis archives

### Custom
- **REST API Client** - Any API with authentication
- **Data Processors** - CSV, JSON analysis

---

## Usage Examples

### Research Agent (with planning)
```
/generate-agent "Research AI healthcare companies - find funding and technology advantages"

Gets:
✓ Planning tools (strategy)
✓ Web search (discovery)
✓ Analysis tools
```

### Market Analysis (with evaluation)
```
/generate-agent "Analyze stocks for unusual patterns and rank top performers"

Gets:
✓ Planning tools (approach)
✓ Finnhub (data)
✓ Evaluation framework
```

### Problem Solving (with iteration)
```
/generate-agent "Identify system bottlenecks and propose solutions"

Gets:
✓ Planning tools (decomposition)
✓ Refinement tools (iteration)
✓ Evaluation framework
```

---

## Key Difference: Always Planning

Unlike generic agents, DeepAgents always include planning:
1. **Plan** the approach
2. **Decompose** into steps
3. **Execute** with tools
4. **Evaluate** results
5. **Refine** based on feedback

Planning tools are built-in and automatic. Just describe what you need analyzed!
