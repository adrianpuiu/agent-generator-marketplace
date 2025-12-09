---
description: Create a multi-agent team with coordinator and specialist workers for parallel processing and complex tasks
argument-hint: "[task description or domain]"
---

# Multi-Agent Team

Generate a team of coordinated DeepAgents: a coordinator that plans and delegates, specialist workers that execute in parallel, and reporters that synthesize findings.

## Perfect For

- Parallel analysis of multiple items (stocks, companies, products)
- Distributed data processing
- Multi-perspective evaluation
- Coordinated research across domains
- Portfolio/batch analysis
- Large-scale monitoring and alerts

## Usage

```
/multi-agent-team "Monitor 100 stocks for unusual trading patterns and flag anomalies"
```

With options:

```
/multi-agent-team "task" --num-agents 10
/multi-agent-team "task" --num-agents 10 --memory redis
/multi-agent-team "task" --batch-size 5
```

## What You Get

Generated multi-agent system includes:

✅ **Coordinator Agent**
- Plans work distribution
- Delegates to specialists
- Manages execution
- Handles failures

✅ **Specialist Worker Agents** (parallel)
- Execute domain tasks
- Process sub-problems
- Generate local insights
- Report back findings

✅ **Aggregator Agent**
- Combines results
- Identifies patterns
- Synthesizes insights
- Generates unified report

✅ **Alert/Reporter Agent** (optional)
- Flags high-priority findings
- Generates summary reports
- Ranks results by importance

## Workflow

1. **Coordinator Plans** - Break large task into sub-tasks
2. **Distribute Work** - Assign to N worker agents
3. **Workers Execute** - Parallel processing
4. **Collect Results** - Gather worker outputs
5. **Aggregate** - Synthesize findings
6. **Alert/Report** - Generate unified output

## Real Examples

### Example 1: Stock Monitoring
```
/multi-agent-team "Monitor 100 stocks for unusual patterns" --num-agents 10

Generated system:
- Coordinator: Divides 100 stocks into 10 batches
- 10 Worker Agents: Analyze 10 stocks each in parallel
  - Technical patterns
  - Volume anomalies
  - Sentiment analysis
  - Price prediction
- Aggregator: Combines results
- Reporter: Generates alerts and rankings
```

### Example 2: Competitive Analysis
```
/multi-agent-team "Analyze 50 AI companies across 5 dimensions" --num-agents 5

Generated system:
- Coordinator: Plans analysis across dimensions
- Worker 1: Technology analysis (all 50 companies)
- Worker 2: Funding analysis (all 50 companies)
- Worker 3: Team/People analysis (all 50 companies)
- Worker 4: Product positioning (all 50 companies)
- Worker 5: Market opportunity (all 50 companies)
- Aggregator: Combines into unified competitive matrix
- Reporter: Generates market landscape report
```

### Example 3: Data Processing Pipeline
```
/multi-agent-team "Process 1M customer records for segmentation" --num-agents 20

Generated system:
- Coordinator: Splits into 20 batches (50k records each)
- 20 Worker Agents: Process batches in parallel
  - Data cleaning
  - Feature extraction
  - Anomaly detection
  - Segment assignment
- Aggregator: Combines segments, resolves boundaries
- Reporter: Generates segmentation report and insights
```

## Options

- `--num-agents 10` - Number of parallel worker agents (default: 5)
- `--batch-size 10` - Items per agent (auto-calculated from num-agents)
- `--memory redis` - Enable Redis for long operations
- `--timeout 3600` - Per-agent timeout in seconds

## After Generation

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run team
python generated_agent.py "items_to_process.json"

# 3. Output
- coordinator_plan.md - Task breakdown
- worker_results/ - Individual worker findings
  - worker_1_results.json
  - worker_2_results.json
  - ...
- aggregated_report.md - Combined findings
- alerts.json - High-priority items
- summary_report.txt - Executive summary
```

## Key Features

- **Parallel Processing** - Process 10-100+ items simultaneously
- **Scalable** - Add more workers for more items
- **Coordinated** - Central planning and aggregation
- **Resilient** - Worker failures don't stop system
- **Flexible** - Customize worker specialization
- **Observable** - Track each worker's progress

## Architecture

```
┌─────────────────────────────────────────┐
│      Coordinator Agent (Planning)       │
│  - Break task into N sub-tasks          │
│  - Assign to workers                    │
│  - Track progress                       │
└──────────────┬──────────────────────────┘
               │
       ┌───────┼───────┬─────────┐
       │       │       │         │
    Worker  Worker  Worker   Worker
    Agent 1 Agent 2 Agent 3  Agent N
    
    [Parallel execution]
    
       │       │       │         │
       └───────┼───────┴─────────┘
               │
┌──────────────▼──────────────────────────┐
│    Aggregator Agent (Synthesis)         │
│  - Combine results                      │
│  - Find patterns                        │
│  - Resolve conflicts                    │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│  Reporter Agent (Output)                │
│  - Generate alerts                      │
│  - Create reports                       │
│  - Rank findings                        │
└──────────────────────────────────────────┘
```

## Customization

- Customize worker specialization
- Add inter-agent communication
- Implement custom aggregation logic
- Add filtering and ranking
- Deploy on distributed systems
- Integrate with monitoring tools

## Use Cases

- **Finance** - Portfolio monitoring, stock analysis
- **Sales** - Territory analysis, lead scoring
- **Marketing** - Campaign analysis across segments
- **Operations** - Equipment monitoring, fleet analysis
- **Risk** - Threat detection, anomaly monitoring
- **Research** - Literature review, data exploration
- **E-commerce** - Product analysis, pricing optimization

## Performance

- 5 agents: ~10-50 items
- 10 agents: ~50-100 items
- 20 agents: ~100-500 items
- Scale horizontally based on needs

## Cost Considerations

- Each worker agent = 1 API call allocation
- Coordinator + Aggregator overhead
- Redis for state management (if enabled)
- Budget N+2 tokens for N workers
