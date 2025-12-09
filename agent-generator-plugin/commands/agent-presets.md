---
description: Configure agent presets for different use cases - fast, thorough, or collaborative
argument-hint: "[command] [preset]"
---

# Agent Presets

Configure pre-built presets that optimize agents for specific scenarios. Use `--preset` flag with any agent command to apply optimization.

## Available Presets

### 1. `--preset fast`
**Optimized for:** Speed, quick results, MVP validation

Features:
- Fewer iterations (3 instead of 15)
- Shorter planning cycles
- Basic tools only
- Quick output formatting
- 2-3 minutes typical execution

Best for:
- Quick exploratory research
- Rapid prototyping
- Initial feasibility checks
- Time-constrained decisions

```bash
/research-agent "quantum companies" --preset fast
/analysis-agent "stock data" --preset fast
/problem-solver "optimize API" --preset fast
```

### 2. `--preset thorough` (Default)
**Optimized for:** Quality, depth, comprehensive analysis

Features:
- Full iterations (15+)
- Deep planning and refinement
- All available tools
- Comprehensive output
- 10-20 minutes typical execution

Best for:
- Investment decisions
- Critical system analysis
- Strategic planning
- Publication-quality work

```bash
/research-agent "quantum companies" --preset thorough
/analysis-agent "stock data" --preset thorough
/problem-solver "optimize API" --preset thorough
```

### 3. `--preset collaborative`
**Optimized for:** Team coordination, parallel processing, aggregated insights

Features:
- Multi-agent architecture
- Worker specialization
- Cross-team validation
- Consensus building
- Unified reporting

Best for:
- Large teams analyzing same topic
- Need for multiple perspectives
- Risk mitigation (validation)
- Distributed teams
- Complex interdisciplinary problems

```bash
/research-agent "quantum companies" --preset collaborative --num-workers 5
/multi-agent-team "analyze market" --preset collaborative --num-agents 10
```

---

## Preset Comparison

| Aspect | Fast | Thorough | Collaborative |
|--------|------|----------|---------------|
| **Iterations** | 3 | 15 | 10-15 per agent |
| **Tools** | Core only | All | Specialized per worker |
| **Time** | 2-3 min | 10-20 min | 15-30 min |
| **Quality** | Good | Excellent | Very good (multiple views) |
| **Cost** | Low | Medium | High (N+2 agents) |
| **Use Case** | Quick check | Deep work | Complex/Risk |

---

## How to Use

### Basic Usage
```bash
# Use thorough preset (default)
/research-agent "topic"

# Use fast preset
/research-agent "topic" --preset fast

# Use thorough preset explicitly
/research-agent "topic" --preset thorough

# Use collaborative preset
/multi-agent-team "task" --preset collaborative --num-agents 5
```

### With Other Options
```bash
# Combine presets with memory and other options
/research-agent "topic" --preset fast --memory redis

/analysis-agent "goal" --preset thorough --memory redis --visualize yes

/problem-solver "problem" --preset collaborative --memory redis --num-solutions 5

/multi-agent-team "task" --preset collaborative --num-agents 10 --memory redis
```

---

## Preset Details

### Fast Preset Configuration

```python
{
    "max_iterations": 3,
    "planning_depth": "quick",
    "tools": ["core_tools"],
    "output_format": "concise",
    "memory": "memory",  # No Redis needed
    "timeout": 180,  # 3 minutes
    "model": "claude-sonnet-4",  # Standard model
}
```

**Best for Quick Research:**
```bash
/research-agent "What's the latest in AI?" --preset fast
# Result: Quick overview (2-3 min)
```

### Thorough Preset Configuration

```python
{
    "max_iterations": 15,
    "planning_depth": "comprehensive",
    "tools": ["all_tools"],
    "output_format": "detailed",
    "memory": "memory",  # or "redis"
    "timeout": 1200,  # 20 minutes
    "model": "claude-sonnet-4",
}
```

**Best for Deep Research:**
```bash
/research-agent "Comprehensive analysis of quantum computing market" --preset thorough
# Result: Detailed report (10-20 min)
```

### Collaborative Preset Configuration

```python
{
    "coordinator_iterations": 10,
    "worker_iterations": 10,
    "num_agents": 5,  # or specify with --num-agents
    "worker_specialization": True,
    "aggregation_depth": "comprehensive",
    "consensus_building": True,
    "output_format": "unified_with_perspectives",
    "memory": "redis",  # Required for coordination
}
```

**Best for Team Analysis:**
```bash
/multi-agent-team "Analyze 5 markets" --preset collaborative --num-agents 5
# Result: Coordinated analysis with multiple perspectives
```

---

## Real-World Examples

### Example 1: Fast vs Thorough Research

**Quick Decision:**
```bash
/research-agent "Should we invest in Company X?" --preset fast
# 2-3 minutes
# Output: Quick assessment, yes/no decision
```

**Deep Due Diligence:**
```bash
/research-agent "Complete due diligence on Company X" --preset thorough
# 15-20 minutes
# Output: Comprehensive report, all angles covered
```

### Example 2: Fast vs Thorough Problem-Solving

**Quick Fix:**
```bash
/problem-solver "API is slow" --preset fast
# 2-3 minutes
# Output: Immediate optimization suggestions
```

**Comprehensive Solution:**
```bash
/problem-solver "Optimize entire system performance" --preset thorough
# 15-20 minutes
# Output: Complete RCA with prioritized solutions
```

### Example 3: Solo vs Collaborative Analysis

**Individual Analysis:**
```bash
/analysis-agent "Analyze market trends" --preset thorough
# Single perspective, comprehensive
# Output: One analyst's findings
```

**Team Analysis:**
```bash
/analysis-agent "Analyze market trends" --preset collaborative --num-agents 5
# 5 specialized analysts, different angles
# Output: Unified report with multiple perspectives
```

---

## Cost Considerations

### API Call Cost by Preset

| Preset | Agents | Iterations | Approx Calls | Cost Relative |
|--------|--------|-----------|--------------|--------------|
| Fast | 1 | 3 | ~30 | 1x |
| Thorough | 1 | 15 | ~150 | 5x |
| Collaborative (5) | 5 | 10 | ~500 | 17x |
| Collaborative (10) | 10 | 10 | ~1000 | 33x |

**Note:** Costs are estimates. Actual costs depend on input/output size.

---

## Recommendation Flowchart

```
Need quick answer?
├─ YES → Use --preset fast
│
Need comprehensive analysis?
├─ YES → Use --preset thorough
│
Need team validation/multiple perspectives?
├─ YES → Use --preset collaborative
│
Uncertain?
└─ Use --preset thorough (default, highest quality)
```

---

## Combining Presets with Memory

### Fast + In-Memory
```bash
/research-agent "topic" --preset fast
# Quick, no external dependencies needed
```

### Thorough + Redis
```bash
/research-agent "topic" --preset thorough --memory redis
# Deep analysis, persistent session state
```

### Collaborative + Redis
```bash
/multi-agent-team "task" --preset collaborative --num-agents 10 --memory redis
# Team coordination, persistent worker state
```

---

## Advanced: Custom Preset Creation

Users can create custom presets by modifying generated agent code:

```python
# In generated_agent.py
custom_preset = {
    "max_iterations": 20,  # Very thorough
    "planning_depth": "exhaustive",
    "tools": ["all_tools"],
    "output_format": "publication_quality",
    "memory": "postgres",  # For archival
}

agent = create_deep_agent(
    model="claude-sonnet-4-20250514",
    tools=tools,
    max_iterations=custom_preset["max_iterations"],
    # ... more configuration
)
```

---

## Performance Expectations

### Fast Preset (3 iterations, 2-3 min)
```
Iteration 1: Initial analysis
Iteration 2: Quick refinement
Iteration 3: Final output
Done!
```

### Thorough Preset (15 iterations, 10-20 min)
```
Iterations 1-3: Initial analysis
Iterations 4-9: Deep investigation
Iterations 10-12: Refinement
Iterations 13-15: Final validation
Done!
```

### Collaborative Preset (5 agents, 10 iterations each)
```
Coordinator: Plan work (1 iteration)
Workers: Analysis in parallel (10 iterations each)
Aggregator: Combine results (2 iterations)
Reporter: Generate output (1 iteration)
Done!
```

---

## When to Change from Default

**Switch to `--preset fast` when:**
- You just need a quick answer
- Time is critical
- This is early exploration
- You need MVP validation
- Budget is tight

**Switch to `--preset thorough` when:**
- Quality matters most (default)
- Decision is important
- Publication or presentation
- You have time available
- Budget allows

**Switch to `--preset collaborative` when:**
- You need multiple perspectives
- Risk mitigation is critical
- Team needs alignment
- Complex interdisciplinary problem
- You have a team to distribute work

---

## Tips & Best Practices

1. **Start with Fast** - Quick exploration
2. **Scale to Thorough** - When you find something important
3. **Use Collaborative** - For critical decisions with teams
4. **Combine with Memory** - Enable Redis for long sessions
5. **Document Results** - Save outputs for reference

---

## Troubleshooting

**"Agent is taking too long"**
→ Use `--preset fast` instead

**"Results don't seem thorough enough"**
→ Use `--preset thorough` instead

**"I need consensus from team"**
→ Use `--preset collaborative` with multiple agents

**"I'm getting timeout errors"**
→ Use `--preset fast` or increase timeout with `--timeout 3600`

---

## Summary

| Need | Preset | Time | Quality |
|------|--------|------|---------|
| Quick check | fast | 2-3 min | Good |
| Good work | thorough | 10-20 min | Excellent |
| Team validation | collaborative | 15-30 min | Very good + multi-perspective |

**Default is `thorough` - best for most work.**
