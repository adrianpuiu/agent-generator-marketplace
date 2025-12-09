# Advanced Memory Patterns for DeepAgents

Specialized memory configurations for different agent use cases and workflows.

## Memory Backends

### 1. In-Memory (Default)
```python
{
    "type": "memory",
    "cache": "in_process",
}
```

**Use When:**
- Development/testing
- Single-session agents
- No persistence needed
- Quick prototyping

**Pros:** No external dependencies, simple
**Cons:** Lost on restart, single-machine only

---

### 2. Redis (Distributed Memory)
```python
{
    "type": "redis",
    "url": "redis://localhost:6379/0",
    "ttl": 86400,  # 24 hours
    "key_prefix": "agent:",
    "compression": True,
}
```

**Use When:**
- Long-running research sessions
- Team collaboration
- Distributed agents
- Session persistence needed

**Configuration:**
- `ttl` - Session timeout (default: 24 hours)
- `key_prefix` - Namespace for agent data
- `compression` - Reduce memory usage

**Best for:** Research agents, multi-day analysis

---

### 3. PostgreSQL (Persistent Storage)
```python
{
    "type": "postgres",
    "url": "postgresql://user:password@localhost/agents_db",
    "table_name": "agent_state",
    "archive": True,
    "version_control": True,
}
```

**Use When:**
- Permanent record needed
- Audit trails required
- Complex query analysis
- Large-scale deployment

**Configuration:**
- `archive` - Keep old versions
- `version_control` - Track all changes
- `table_name` - Custom table name

**Best for:** Enterprise, compliance, historical analysis

---

## Advanced Memory Patterns

### Pattern 1: Research Session Memory

For long-running research with multiple refinements:

```python
memory_config = {
    "type": "redis",
    "ttl": 604800,  # 7 days
    "store_intermediate_plans": True,
    "store_sub_agent_results": True,
    "compress_old_iterations": True,
    "key_structure": {
        "session": "research_session_{session_id}",
        "plans": "research_session_{session_id}:plans",
        "findings": "research_session_{session_id}:findings",
        "sources": "research_session_{session_id}:sources",
    }
}
```

**Stores:**
- All planning iterations
- Research findings at each stage
- Source evaluation results
- Final thesis with evidence

**Workflow:**
```
Session Start → Plan → Search → Analyze → Refine → Store
                         ↓
                      (iterate)
                         ↓
Session End → Archive → Close
```

---

### Pattern 2: Multi-Agent Coordination Memory

For teams of coordinated agents:

```python
memory_config = {
    "type": "redis",
    "ttl": 86400,
    "coordination_mode": True,
    "worker_result_aggregation": True,
    "key_structure": {
        "coordinator": "coordinator_{task_id}",
        "workers": "workers_{task_id}:{worker_id}",
        "results": "results_{task_id}:aggregated",
        "state": "state_{task_id}:shared",
    },
    "shared_state": {
        "task_definition": {},
        "work_distribution": [],
        "worker_status": {},
        "aggregated_results": {},
    }
}
```

**Stores:**
- Coordinator's work plan
- Each worker's task and progress
- Shared state for all workers
- Aggregated results

**Workflow:**
```
Coordinator Plan → Distribute → Workers Execute (parallel)
                                    ↓
                             Share intermediate results
                                    ↓
                              Aggregate → Final Report
```

---

### Pattern 3: Analysis Versioning

Track multiple analysis iterations with full history:

```python
memory_config = {
    "type": "postgres",
    "archive": True,
    "version_control": True,
    "key_structure": {
        "analysis_id": "analysis_{timestamp}_{id}",
        "iterations": "analysis_{id}:iterations",
        "versions": "analysis_{id}:versions",
        "metadata": "analysis_{id}:metadata",
    },
    "track_changes": {
        "store_before_after": True,
        "store_diffs": True,
        "store_confidence_levels": True,
        "store_reasoning": True,
    }
}
```

**Stores:**
- Complete analysis history
- All iterations with changes
- Confidence levels per finding
- Reasoning for each decision

**Workflow:**
```
Initial Analysis → Iteration 1 (v0.1) → Iteration 2 (v0.2) → Iteration 3 (v1.0)
   Document          Archive changes      Update metadata      Publish
```

---

### Pattern 4: Sub-Agent Memory Hierarchy

Coordinated memory for agent teams with specialization:

```python
memory_config = {
    "type": "redis",
    "hierarchy": True,
    "ttl": 86400,
    "key_structure": {
        # Global coordination
        "global": "team_{team_id}:global",
        
        # Team-level
        "team": "team_{team_id}:state",
        
        # Agent-level (specialized)
        "research_agent": "team_{team_id}:agent_research:state",
        "analysis_agent": "team_{team_id}:agent_analysis:state",
        "coordinator_agent": "team_{team_id}:agent_coord:state",
        
        # Results
        "team_results": "team_{team_id}:results:aggregated",
    },
    "propagation": {
        "global_to_team": True,
        "team_to_agent": True,
        "agent_to_results": True,
    }
}
```

**Memory Hierarchy:**
```
┌─ Global Team State
│  ├─ Team Shared State
│  │  ├─ Research Agent Memory
│  │  ├─ Analysis Agent Memory
│  │  └─ Coordinator Memory
│  └─ Aggregated Results
```

---

### Pattern 5: Compression & Cleanup

Optimize storage for long-running agents:

```python
memory_config = {
    "type": "redis",
    "ttl": 604800,  # 7 days
    "compression": {
        "enabled": True,
        "compress_after_iterations": 5,
        "compression_level": "high",
    },
    "cleanup": {
        "auto_cleanup": True,
        "cleanup_interval": 3600,  # 1 hour
        "keep_last_n_versions": 10,
    },
    "archival": {
        "archive_old_sessions": True,
        "archive_threshold": 86400,  # 1 day old
        "postgres_archive": True,
    }
}
```

**Features:**
- Compress old iterations
- Auto-cleanup expired data
- Archive to PostgreSQL
- Configurable retention

---

## Use Case Patterns

### Use Case: Investment Research (7-Day Deep Dive)

```python
# Research agent analyzing a company
memory_config = {
    "type": "redis",
    "ttl": 604800,  # 7 days
    "store_intermediate_plans": True,
    "store_sub_agent_results": True,
    "track_changes": True,
    "key_structure": {
        "session": f"research_company_{company_id}_{date}",
        "plans": f"research_company_{company_id}:plans",
        "findings": f"research_company_{company_id}:findings",
        "sources": f"research_company_{company_id}:sources",
    }
}

# Workflow:
# Day 1: Initial research plan + web search
# Day 2: Deep dive into technology
# Day 3: Funding analysis
# Day 4: Team & market analysis
# Day 5: Competitive positioning
# Day 6: Refine thesis
# Day 7: Final report generation
# → All intermediate results persisted
```

### Use Case: Coordinated Team Analysis (24 Hours)

```python
# Multi-agent team analyzing market
memory_config = {
    "type": "redis",
    "ttl": 86400,  # 24 hours
    "coordination_mode": True,
    "shared_state": {
        "market": {},
        "competitors": {},
        "opportunities": {},
    },
    "key_structure": {
        "coordinator": "market_analysis_coord",
        "workers": "market_analysis_workers:{id}",
        "results": "market_analysis_results:final",
    }
}

# 5-Agent Team:
# Agent 1: Market analysis
# Agent 2: Competitor analysis
# Agent 3: Opportunity analysis
# Agent 4: Risk analysis
# Agent 5: Coordinator/Aggregator
# → All share state and coordinate
```

### Use Case: Audit Trail (Permanent Record)

```python
# Analysis with full audit trail
memory_config = {
    "type": "postgres",
    "archive": True,
    "version_control": True,
    "track_changes": {
        "store_before_after": True,
        "store_reasoning": True,
        "store_confidence": True,
    }
}

# Stores:
# - Initial analysis (v1.0)
# - All changes with reasons
# - Confidence scores
# - Complete audit trail
# - Permanent archive
```

---

## Memory Configuration Best Practices

### 1. Choose Backend by Use Case
```python
# Development: In-Memory
if environment == "development":
    backend = "memory"

# Production Single-Agent: Redis
elif num_agents == 1:
    backend = "redis"

# Production Multi-Agent: Redis + Postgres
elif num_agents > 1:
    backend = "redis"
    archive_backend = "postgres"
```

### 2. Set Appropriate TTL
```python
# Quick analysis: 1 hour
ttl_quick = 3600

# Research session: 24 hours
ttl_research = 86400

# Deep project: 7 days
ttl_project = 604800

# Permanent: Postgres (no TTL)
```

### 3. Enable Compression for Long Sessions
```python
if session_duration > 86400:  # More than 1 day
    enable_compression = True
    compress_after_iterations = 5
```

### 4. Use Postgres for Compliance
```python
if compliance_required or audit_trail_needed:
    use_postgres = True
    enable_version_control = True
    track_all_changes = True
```

### 5. Configure Shared State for Teams
```python
if num_agents > 1:
    enable_shared_state = True
    shared_state_sync = True  # Sync between agents
```

---

## Performance Optimization

### For Fast Agents (--preset fast)
```python
memory_config = {
    "type": "memory",  # No network overhead
    "compression": False,  # Not needed for short sessions
}
```

### For Thorough Agents (--preset thorough)
```python
memory_config = {
    "type": "redis",
    "ttl": 86400,
    "compression": True,  # Compress after 5 iterations
}
```

### For Collaborative Agents (--preset collaborative)
```python
memory_config = {
    "type": "redis",
    "ttl": 86400,
    "coordination_mode": True,
    "shared_state": {...},
}
```

---

## Cost Optimization

### Reduce Cost with:
1. Use in-memory for short sessions
2. Set realistic TTL (don't keep forever)
3. Enable compression
4. Clean up old data regularly
5. Use Postgres only when necessary

### Monitor Usage with:
```python
# In Redis
DBSIZE  # Check memory usage
INFO memory  # Detailed memory stats
KEYS pattern:*  # List all keys
TTL key  # Check expiration
```

---

## Examples

See `redis_memory.md` for Redis-specific configuration.

See generated agent code for implementation examples.
