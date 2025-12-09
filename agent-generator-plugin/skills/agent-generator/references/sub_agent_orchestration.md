# Sub-Agent Orchestration Guide

Framework for creating and coordinating teams of specialized DeepAgents working in parallel.

## Concepts

### Single Agent
```
Task → [Single DeepAgent] → Result
```
- Simple, focused
- Good for single-perspective analysis
- Limited scalability

### Multi-Agent Team (Coordinated)
```
        ┌─ [Worker Agent 1]
Task →  ├─ [Worker Agent 2]  (parallel) → [Aggregator] → Result
        ├─ [Worker Agent 3]
        └─ [Worker Agent N]
```
- Parallel processing
- Multiple perspectives
- Scalable to 100+ items

---

## Agent Roles

### Coordinator Agent
**Responsibilities:**
- Parse incoming task
- Decompose into sub-tasks
- Create work distribution plan
- Delegate to workers
- Manage worker execution
- Handle failures/retries

**Tools:**
- `plan_work_distribution()` - Create work plan
- `spawn_worker_agents()` - Create worker instances
- `track_progress()` - Monitor execution
- `handle_failure()` - Manage errors

---

### Worker Agents
**Responsibilities:**
- Execute assigned sub-task
- Process local data
- Generate local insights
- Report back results
- Handle edge cases

**Architecture:**
- Each worker is a full DeepAgent
- Specialized for sub-domain
- Can run in parallel
- Isolated execution state

**Specializations:**
```python
workers = {
    "research": ResearchWorker(),  # Web search + analysis
    "analysis": AnalysisWorker(),  # Data exploration
    "evaluation": EvalWorker(),    # Solution ranking
    "reporting": ReporterAgent(),  # Output generation
}
```

---

### Aggregator Agent
**Responsibilities:**
- Collect worker results
- Combine and deduplicate
- Identify patterns across results
- Resolve conflicts
- Generate unified findings

**Tools:**
- `aggregate_results()` - Combine outputs
- `identify_patterns()` - Find cross-agent patterns
- `resolve_conflicts()` - Handle disagreements
- `generate_summary()` - Create unified report

---

## Orchestration Patterns

### Pattern 1: Data Parallelization
Split data across workers, each processes portion:

```python
# Task: Analyze 100 stocks
# Workers: 10 agents

# Distribution:
# Worker 1: Stocks 1-10
# Worker 2: Stocks 11-20
# ...
# Worker 10: Stocks 91-100

# Aggregation:
# Combine all analyses
# Find patterns across stocks
# Generate unified rankings
```

**Use When:**
- Processing 100+ similar items
- Each item independent
- Results need aggregation

---

### Pattern 2: Functional Specialization
Each worker specializes in different aspect:

```python
# Task: Analyze company completely
# Workers: 5 specialized agents

# Worker 1: Technology analysis
# Worker 2: Market analysis
# Worker 3: Financial analysis
# Worker 4: Team/People analysis
# Worker 5: Competitive analysis

# Aggregation:
# Combine all perspectives
# Create holistic view
# Generate comprehensive assessment
```

**Use When:**
- Multi-dimensional analysis needed
- Experts in different domains
- Need integrated perspective

---

### Pattern 3: Hierarchical Decomposition
Multi-level task breakdown:

```python
# Level 1: Coordinator plans work
#
# Level 2: Team leads manage specialists
# - Research Team Lead
# - Analysis Team Lead
# - Evaluation Team Lead
#
# Level 3: Individual specialists
# - Research: Web search, gathering
# - Analysis: Data processing
# - Evaluation: Ranking solutions
#
# Aggregation: Bottom-up integration
```

**Use When:**
- Very large tasks
- Many workers needed
- Complex coordination

---

## Execution Flow

### Sequential Coordination
```
Coordinator Plans
      ↓
Workers Execute (one at a time)
      ↓
Aggregator Combines
      ↓
Result
```
**Use When:** Coordination overhead is high, few workers

### Parallel Coordination
```
Coordinator Plans
      ↓
Workers Execute (simultaneously)
      ↓
Aggregator Combines (as results arrive)
      ↓
Result
```
**Use When:** Workers are independent, many workers

### Staged Coordination
```
Coordinator Plans
      ↓
Stage 1: Research workers (parallel)
      ↓
Stage 2: Analysis workers (wait for research)
      ↓
Stage 3: Evaluation workers (wait for analysis)
      ↓
Aggregator Combines
      ↓
Result
```
**Use When:** Dependencies between stages

---

## Communication Patterns

### Worker to Coordinator
```
Worker Reports:
- Task progress
- Intermediate results
- Errors/exceptions
- Estimated completion time

Coordinator:
- Receives reports
- Tracks progress
- Handles failures
- Triggers next stage
```

### Worker to Worker (via Shared State)
```
Shared Redis State:
- Common context
- Progress tracking
- Intermediate findings
- Coordination flags

Workers:
- Read shared state
- Write findings
- Update progress
- Signal completion
```

### Aggregator Communication
```
Aggregator Receives:
- All worker results
- Intermediate reports
- Final outputs

Aggregator Outputs:
- Unified findings
- Cross-worker patterns
- Ranked results
- Final report
```

---

## Example: Stock Analysis Team

### Setup
```python
# Task: Analyze 100 stocks
# Team Size: 10 workers

coordinator = create_coordinator_agent(
    num_workers=10,
    items_per_worker=10,  # 100 stocks / 10 workers
)

workers = [
    create_analysis_worker(f"worker_{i}", 
                          stocks[i*10:(i+1)*10])
    for i in range(10)
]

aggregator = create_aggregator_agent()
```

### Execution
```python
async def run_stock_analysis():
    # 1. Coordinator plans work
    plan = await coordinator.plan_work(
        task="Analyze 100 stocks",
        num_workers=10
    )
    
    # 2. Workers analyze in parallel
    results = await asyncio.gather(
        *[worker.analyze_stocks() for worker in workers]
    )
    
    # 3. Aggregator combines results
    final_report = await aggregator.aggregate(
        worker_results=results,
        analysis_type="stock_patterns"
    )
    
    return final_report
```

### Results
```
Output:
- worker_1_analysis.json (stocks 1-10)
- worker_2_analysis.json (stocks 11-20)
- ...
- worker_10_analysis.json (stocks 91-100)
- aggregated_findings.md (patterns across all)
- alerts.json (anomalies flagged)
- summary_report.txt (executive overview)
```

---

## Scaling Guidelines

| Team Size | Items | Execution | Memory | Coordination |
|-----------|-------|-----------|--------|--------------|
| 1 agent | 1 | Sequential | Low | None |
| 5 agents | 50 | Parallel | Medium | Shared state |
| 10 agents | 100 | Parallel | High | Shared state |
| 20 agents | 500 | Parallel | Very High | Distributed |
| 50+ agents | 1000+ | Distributed | Very High | Kubernetes |

---

## Error Handling

### Worker Failure Scenarios
```python
# Scenario 1: Single worker fails
# → Reassign to backup worker
# → Continue other workers
# → Aggregator notes incomplete data

# Scenario 2: Multiple workers fail
# → Coordinator retries failed tasks
# → If retries exceed limit, report failure
# → Aggregator uses partial results

# Scenario 3: Aggregator fails
# → Save individual worker results
# → Manual aggregation
# → Report for human review
```

### Recovery Strategies
```python
# Automatic Retry
max_retries = 3
retry_backoff = 2  # Exponential backoff

# Fallback Agents
if worker_fails:
    use_backup_worker()
    
# Partial Results
if some_workers_fail:
    aggregated_results = aggregate_partial(workers_who_succeeded)
    
# Human Intervention
if critical_failure:
    notify_human_operator()
```

---

## Performance Optimization

### 1. Load Balancing
```python
# Equal distribution
items_per_worker = total_items / num_workers

# Weighted distribution (by complexity)
worker_capacity = [10, 10, 5, 10]  # Different capacities
distribute_by_capacity(items, worker_capacity)
```

### 2. Batching
```python
# Process in batches to avoid overload
batch_size = 100
num_batches = ceil(total_items / batch_size)

for batch in batches:
    spawn_workers(batch)
    wait_for_completion()
```

### 3. Resource Management
```python
# Limit concurrent workers
max_concurrent = 10

# Queue excess work
pending_queue = Queue()
while pending_queue:
    if active_workers < max_concurrent:
        spawn_worker(pending_queue.pop())
```

---

## Monitoring & Observability

### Metrics to Track
```python
metrics = {
    "coordinator": {
        "plan_time": 2.3,  # seconds
        "work_items": 100,
        "workers_spawned": 10,
    },
    "workers": {
        "active": 10,
        "completed": 7,
        "failed": 0,
        "avg_time": 45.2,  # seconds
    },
    "aggregator": {
        "start_time": "2024-12-09T14:30:00Z",
        "items_received": 10,
        "items_processed": 10,
        "total_time": 240.5,  # seconds
    }
}
```

### Logging
```python
# Coordinator logs
logger.info(f"Spawning {num_workers} workers")
logger.info(f"Distributing {num_items} items")

# Worker logs
logger.info(f"Worker {id} starting task")
logger.info(f"Worker {id} completed {num_completed} items")

# Aggregator logs
logger.info(f"Aggregating {num_results} results")
logger.info(f"Found {num_patterns} patterns")
```

---

## When to Use Sub-Agent Teams

### Use Multi-Agent When:
✓ Processing 50+ items
✓ Need multiple perspectives
✓ Data is parallelizable
✓ Speed is important
✓ Complex analysis needed
✓ Team collaboration beneficial

### Use Single Agent When:
✓ Simple task
✓ <50 items
✓ Single perspective enough
✓ Quality > speed
✓ Cost is critical
✓ Coordination overhead too high

---

## Advanced: Custom Orchestration

Users can implement custom orchestration by modifying the multi_agent_template.py:

```python
class CustomOrchestrator:
    async def custom_workflow(self):
        # 1. Coordinator plans
        plan = await self.coordinator.plan()
        
        # 2. Custom worker assignment
        assignments = await self.custom_distribute(plan)
        
        # 3. Workers execute
        results = await asyncio.gather(
            *[worker.execute(task) for task in assignments]
        )
        
        # 4. Custom aggregation
        final = await self.custom_aggregate(results)
        
        return final
```

---

## Summary

**Multi-Agent Orchestration enables:**
- Parallel processing of 100+ items
- Multiple specialized perspectives
- Scalable architecture
- Resilient to failures
- Professional-quality results

**Key Components:**
1. Coordinator (planning & delegation)
2. Workers (parallel execution)
3. Aggregator (result synthesis)
4. Shared State (coordination)
5. Error Handling (resilience)

**Best Practices:**
- Plan work clearly
- Monitor progress
- Handle failures gracefully
- Aggregate comprehensively
- Scale incrementally
