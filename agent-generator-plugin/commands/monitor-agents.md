---
description: Monitor agent performance, execution metrics, and results in real-time with dashboards and alerts
argument-hint: "[agent_id or 'all']"
---

# Monitor Agents

Real-time monitoring of agent execution, performance metrics, and result quality. Create dashboards, set alerts, and track agent teams.

## Basic Usage

```bash
# Monitor all agents
/monitor-agents all

# Monitor specific agent
/monitor-agents "research_agent_001"

# Monitor with dashboard
/monitor-agents all --dashboard yes --refresh 30s
```

## Monitoring Views

### 1. Execution Metrics

Track real-time execution data:

```bash
/monitor-agents all --metrics execution
```

**Metrics tracked:**
- Iterations completed
- Current iteration progress
- Estimated time remaining
- Resource usage (CPU, memory)
- Token consumption
- Cost tracking

**Real-time Display:**
```
Agent: research_agent_001
Status: Running (Iteration 8/15)
Progress: 53%
Elapsed: 7m 23s
Estimated: 13m remaining
Cost: $0.42 / $0.80 budget
Tokens: 45K / 100K
```

---

### 2. Result Quality

Monitor result quality in real-time:

```bash
/monitor-agents all --metrics quality
```

**Quality indicators:**
- Data completeness
- Confidence levels
- Finding count
- Evidence coverage
- Validation status

**Display:**
```
Agent: analysis_agent_005
Completeness: 87%
Confidence: High
Findings: 12 key insights
Evidence: 45 sources cited
Status: Refinement phase
```

---

### 3. Team Coordination

Monitor multi-agent team health:

```bash
/monitor-agents all --metrics team
```

**Team metrics:**
- Active workers
- Completed workers
- Failed workers
- Aggregator status
- Shared state sync
- Worker-to-coordinator lag

**Display:**
```
Team: stock_analysis
Active: 8/10
Completed: 6
Failed: 0
Coordinator: Planning
Aggregator: Combining results
Lag: 2.3s
Completion: 60%
```

---

### 4. Performance Dashboard

Interactive dashboard with all metrics:

```bash
/monitor-agents all --dashboard yes --refresh 10s
```

**Dashboard shows:**
- Live execution status
- Performance graphs
- Cost tracking
- Quality metrics
- Team health
- Alert notifications

---

## Real-Time Alerts

Set up alerts for important events:

```bash
# Alert on high cost
/monitor-agents all --alert "cost > $1.00"

# Alert on low quality
/monitor-agents all --alert "confidence < 0.8"

# Alert on failures
/monitor-agents all --alert "status == failed"

# Alert on completion
/monitor-agents all --alert "status == completed"
```

**Alert Actions:**
- Slack notification
- Email notification
- Webhook trigger
- Log entry
- Dashboard highlight

---

## Historical Analysis

Analyze past agent runs:

```bash
# Last 10 runs
/monitor-agents all --history --limit 10

# Today's runs
/monitor-agents all --history --since "today"

# Last week
/monitor-agents all --history --since "7 days ago"

# Compare performance
/monitor-agents all --compare "run_001" "run_002"
```

**Comparison Shows:**
- Execution time differences
- Cost differences
- Quality improvements
- Result differences
- Pattern changes

---

## Cost Tracking

Real-time cost monitoring:

```bash
/monitor-agents all --show-costs yes
```

**Cost breakdown:**
- API calls per agent
- Token consumption
- Integration costs
- Memory/storage costs
- Monthly estimate

**Real Example:**
```
research_agent_001:
  API calls: 150 × $0.003 = $0.45
  Tokens: 125K × $0.000005 = $0.625
  Memory: 2 days × $0.01/day = $0.02
  Total: $1.095

Team total (10 agents): $10.95
Monthly estimate: ~$330
```

---

## Troubleshooting with Monitoring

### Slow Execution
```bash
# Check what's taking time
/monitor-agents agent_id --show-timeline yes

# See iteration breakdown
# Iteration 1: 0.5s (planning)
# Iteration 2: 2.3s (search)
# Iteration 3: 1.8s (analysis)
# ...
```

### Low Quality Results
```bash
# Monitor confidence scores
/monitor-agents agent_id --show-quality detailed

# See which findings are weak
# Finding 1: HIGH confidence (3 sources)
# Finding 2: MEDIUM confidence (1 source)
# Finding 3: LOW confidence (unverified)
```

### Failed Workers (Multi-Agent)
```bash
# Monitor team health
/monitor-agents team_id --show-team detailed

# See which workers failed
# Worker 1: ✓ Complete
# Worker 2: ✗ Failed (timeout)
# Worker 3: ✓ Complete
# Worker 4: ⏳ Running
```

---

## Dashboard Examples

### Dashboard 1: Live Research Agent

```
╔═══════════════════════════════════════════════════════════╗
║ Research Agent: Quantum Computing Market                  ║
╠═══════════════════════════════════════════════════════════╣
║ Status: Running (Iteration 9/15)                          ║
║ Progress: ████████░░░░░░░░░░░░ 45%                       ║
║ Time: 6m 45s / ~15m estimated                             ║
║                                                           ║
║ Quality Metrics:                                          ║
║   Findings: 18  |  Confidence: 82%  |  Sources: 52       ║
║                                                           ║
║ Cost Tracking:                                            ║
║   API Calls: 127 × $0.003 = $0.38                        ║
║   Tokens: 98K × $0.000005 = $0.49                        ║
║   Total: $0.87 / $2.00 budget                            ║
║                                                           ║
║ Recent Events:                                            ║
║   [07:23] Completed finding analysis                     ║
║   [07:18] Retrieved 12 new sources                       ║
║   [07:12] Identified market trends                       ║
╚═══════════════════════════════════════════════════════════╝
```

---

### Dashboard 2: Multi-Agent Team

```
╔═══════════════════════════════════════════════════════════╗
║ Team: Stock Analysis (10 agents)                          ║
╠═══════════════════════════════════════════════════════════╣
║ Status: 7/10 Complete, 1 Running, 2 Queued                ║
║ Overall Progress: ███████░░░░░░░░░░░░░░░ 70%             ║
║ Estimated Completion: 8 minutes                           ║
║                                                           ║
║ Worker Status:                                            ║
║   ✓ Worker 1-7: Complete                                 ║
║   ⏳ Worker 8: Running (Iteration 6/10)                   ║
║   ⏹ Worker 9-10: Queued                                  ║
║                                                           ║
║ Aggregation:                                              ║
║   Findings Received: 210 / 300 expected                  ║
║   Patterns Detected: 14                                  ║
║   Anomalies Flagged: 7                                   ║
║                                                           ║
║ Cost Projection:                                          ║
║   Current: $3.45                                         ║
║   Projected Total: $4.95                                 ║
╚═══════════════════════════════════════════════════════════╝
```

---

## Integration with External Systems

### Datadog Integration
```bash
/monitor-agents all \
  --export datadog \
  --datadog-dashboard "agents-performance" \
  --datadog-tags "team:research,env:prod"
```

### Prometheus Integration
```bash
/monitor-agents all \
  --export prometheus \
  --prometheus-port 9090
```

### CloudWatch Integration
```bash
/monitor-agents all \
  --export cloudwatch \
  --cloudwatch-namespace "CustomAgents"
```

---

## Performance Optimization

Based on monitoring data, optimize:

### If Cost Too High
```bash
# Switch to --preset fast
/agent-type --preset fast

# Reduce iterations
# Limit tools
# Shorter timeouts
```

### If Quality Too Low
```bash
# Switch to --preset thorough
/agent-type --preset thorough

# Enable more tools
# Increase iterations
# Enable memory persistence
```

### If Speed Too Slow
```bash
# Use parallel workers
/multi-agent-team --num-agents 10

# Enable aggressive caching
# Use fast models
# Reduce refinement
```

---

## Alerting Rules

Common alert configurations:

```yaml
alerts:
  - name: "High Cost"
    condition: "cost > budget * 0.8"
    action: "slack:#alerts"
  
  - name: "Low Quality"
    condition: "confidence < 0.75"
    action: "email:team@company.com"
  
  - name: "Agent Failure"
    condition: "status == failed"
    action: ["slack:#alerts", "pagerduty:on-call"]
  
  - name: "Slow Execution"
    condition: "elapsed_time > estimated_time * 1.5"
    action: "slack:#performance"
  
  - name: "Completion"
    condition: "status == completed"
    action: "slack:#results"
```

---

## Best Practices

1. **Monitor Critical Agents** - Important decisions need visibility
2. **Set Cost Alerts** - Prevent budget overruns
3. **Track Quality** - Know when results are weak
4. **Review Historical Data** - Improve future runs
5. **Automate Alerts** - Don't watch dashboards manually
6. **Adjust Based on Metrics** - Optimize as you learn
7. **Share Dashboards** - Team visibility

---

## Summary

**Monitoring provides:**
- ✅ Real-time execution tracking
- ✅ Cost visibility
- ✅ Quality assessment
- ✅ Performance optimization
- ✅ Team coordination insight
- ✅ Historical analysis
- ✅ Automated alerting

**Use For:**
- Live execution visibility
- Cost control
- Quality assurance
- Performance tuning
- Team coordination
- Troubleshooting
- Historical analysis

**Next:** Set up monitoring on your first agent!
