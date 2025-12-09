# Community Templates & Shared Workflows

Pre-built templates, workflows, and configurations shared by the community.

## Template Library

### Financial Analysis Templates

#### Template: "Quarterly Earnings Analysis"
```bash
/research-agent "earnings" --template "quarterly-earnings" \
  --ticker "AAPL" \
  --integrate github,slack
```

**Includes:**
- Earnings metrics research
- Competitor comparison
- Guidance analysis
- Key metrics extraction
- Investment impact assessment

**Output:** earnings_analysis_AAPL_Q4_2024.md

---

#### Template: "Stock Technical Analysis"
```bash
/analysis-agent "technical" --template "stock-technical" \
  --ticker "TSLA" \
  --timeframe "1y" \
  --indicators "SMA,RSI,MACD"
```

**Includes:**
- Technical indicator analysis
- Support/resistance identification
- Pattern recognition
- Trend strength assessment
- Trading signal generation

**Output:** technical_analysis_TSLA.json

---

### Market Research Templates

#### Template: "Competitor Analysis"
```bash
/multi-agent-team "competitors" \
  --template "competitor-analysis" \
  --competitors "OpenAI,Anthropic,Google" \
  --num-agents 3
```

**Includes:**
- Product comparison
- Pricing analysis
- Market positioning
- Technology differentiation
- Go-to-market strategy

**Output:** competitive_landscape.md

---

#### Template: "Market Sizing"
```bash
/research-agent "market-size" --template "market-sizing" \
  --market "AI healthcare" \
  --geography "US,EU,Asia"
```

**Includes:**
- TAM calculation
- SAM derivation
- SOM estimation
- Growth projections
- Market opportunity assessment

**Output:** market_sizing_report.md

---

### Problem-Solving Templates

#### Template: "Root Cause Analysis"
```bash
/problem-solver "rca" --template "root-cause-analysis" \
  --incident "API outage 2024-01-15" \
  --team "engineering"
```

**Includes:**
- Timeline reconstruction
- Contributing factors
- Root cause identification
- Impact assessment
- Prevention recommendations

**Output:** RCA_APIOutage_20240115.md

---

#### Template: "Performance Optimization"
```bash
/problem-solver "optimize" --template "performance-optimization" \
  --system "database" \
  --target_metric "query_latency" \
  --current_value "500ms"
```

**Includes:**
- Bottleneck identification
- Root cause analysis
- Optimization strategies
- Feasibility assessment
- Implementation roadmap

**Output:** optimization_plan.md

---

## Pre-Built Workflows

### Workflow 1: "Weekly Intelligence Report"

```yaml
name: weekly-intelligence
trigger: cron "0 6 * * 1"  # Monday 6 AM

steps:
  1_market_research:
    command: /research-agent "weekly market trends"
    preset: fast
    output: market_trends.md
  
  2_competitor_intel:
    command: /research-agent "competitor news this week"
    preset: fast
    output: competitor_intel.md
  
  3_analyze_data:
    command: /analysis-agent "key metrics analysis"
    preset: fast
    output: metrics_analysis.md
  
  4_compile_report:
    integration: github,slack
    aggregate:
      - market_trends.md
      - competitor_intel.md
      - metrics_analysis.md
    output: weekly_intelligence_report.md
  
  5_notify_team:
    slack:
      channel: "#intelligence"
      message: "Weekly intelligence report ready"
      attach: weekly_intelligence_report.md
```

**Execution Time:** 15 minutes
**Cost:** ~$0.50
**Team:** No manual work

---

### Workflow 2: "Due Diligence Pipeline"

```yaml
name: due-diligence-pipeline
trigger: manual  # Or webhook from Slack

inputs:
  company_name: string
  investment_size: float
  timeline: string  # e.g., "2 weeks"

steps:
  1_company_research:
    command: /research-agent "Company research: {company_name}"
    preset: thorough
    memory: redis
    duration: "20 min"
  
  2_financial_analysis:
    command: /analysis-agent "Financial metrics for {company_name}"
    preset: thorough
    data_source: "financials_api"
    duration: "15 min"
  
  3_competitive_positioning:
    command: /research-agent "Competitive analysis of {company_name}"
    preset: thorough
    duration: "15 min"
  
  4_team_review:
    command: /multi-agent-team "Full assessment of {company_name}"
    num_agents: 4
    specialist_roles: "tech,market,financial,team"
    preset: collaborative
    duration: "20 min"
  
  5_refine_assessment:
    command: /refine-analysis previous_assessment.md
    iterations: 5
    focus: "key risks and opportunities"
    duration: "10 min"
  
  6_generate_memo:
    integration: github,slack
    create_pr: true
    reviewers: ["@investment-team"]
    slack_notify: true

total_time: "80 minutes"
recommended_team: "1 human + agents"
```

---

### Workflow 3: "Continuous Monitoring Setup"

```yaml
name: continuous-monitoring
trigger:
  - schedule: "every 30 minutes"
  - manual_trigger: slack

configuration:
  items_to_monitor: 50
  analysis_per_item: true
  anomaly_detection: true
  alert_threshold: 0.9

steps:
  1_spawn_workers:
    command: /multi-agent-team "Monitor 50 items"
    num_agents: 5
    batch_size: 10
  
  2_real_time_monitoring:
    integrations:
      - datadog  # Metrics
      - slack    # Alerts
      - webhook  # Custom system
    
    alerts:
      - name: "High anomaly score"
        condition: "anomaly_score > 0.85"
        action: ["slack", "email"]
      
      - name: "Critical finding"
        condition: "finding_type == critical"
        action: ["slack:#critical", "pagerduty"]
  
  3_aggregate_results:
    interval: "30 min"
    aggregation: "union + dedup"
  
  4_update_dashboard:
    system: "datadog"
    dashboard: "monitoring-dashboard"
    refresh: "real-time"

features:
  - Real-time monitoring
  - Automatic alerts
  - Historical tracking
  - Trend analysis
  - Anomaly detection
```

---

## Sharing Your Templates

### Template Structure

```
templates/
├── my-template.yaml
├── README.md
├── example_output.md
└── configuration.json
```

### Template Registration

```bash
# Register your template with the community
/template register \
  --name "my-custom-analysis" \
  --path "./templates/my-template.yaml" \
  --description "Custom analysis template" \
  --author "your-name" \
  --license "MIT"

# Template will be available as:
# /agent --template "my-custom-analysis"
```

### Template Marketplace

```bash
# Browse available templates
/template search "financial"

# View template details
/template info "quarterly-earnings"

# Use a template
/research-agent "analysis" --template "quarterly-earnings"

# Rate template
/template rate "quarterly-earnings" 5
```

---

## Real Community Templates

### Template: "AI Company Assessment"

Created by: @research-team (GitHub)
Rating: 4.8/5 (120 ratings)
Used: 450+ times

```bash
/multi-agent-team "ai-company" \
  --template "ai-company-assessment" \
  --company_name "OpenAI" \
  --num_agents 5

# Outputs:
# - Technology assessment
# - Market positioning
# - Funding trajectory
# - Team analysis
# - Competitive threats
# - Investment potential
```

---

### Template: "SaaS Metrics Analysis"

Created by: @product-team (GitHub)
Rating: 4.9/5 (85 ratings)
Used: 320+ times

```bash
/analysis-agent "saas" \
  --template "saas-metrics" \
  --company_name "Stripe" \
  --metrics "MRR,CAC,LTV,Churn" \
  --timeframe "3y"

# Outputs:
# - Metric trends
# - Cohort analysis
# - Benchmarking
# - Growth projections
# - Health score
```

---

### Template: "Weekly Engineering Report"

Created by: @devops-team (GitHub)
Rating: 4.7/5 (95 ratings)
Used: 280+ times

```yaml
# Scheduled workflow
trigger: cron "0 8 * * 1"

workflow:
  - Analyze deployment metrics
  - Review incident reports
  - Track performance trends
  - Generate optimization recommendations
  - Compile executive summary

integration: slack,github
```

---

## Contributing Templates

### Step 1: Create Template

```yaml
# templates/my-analysis.yaml
name: "My Custom Analysis"
version: "1.0"
description: "Analysis template for X"
author: "your-github-handle"
license: "MIT"

agent_config:
  command: "/analysis-agent"
  preset: "thorough"
  memory: "redis"

parameters:
  - name: "data_source"
    type: "string"
    required: true
  
  - name: "focus_area"
    type: "string"
    default: "all"

output_files:
  - "analysis_results.md"
  - "findings.json"
```

### Step 2: Test Template

```bash
# Test locally
/template test "./templates/my-analysis.yaml" \
  --data_source "test_data.csv"
```

### Step 3: Share Template

```bash
# Push to GitHub
git push origin feature/my-analysis-template

# Create pull request to community templates repo
# https://github.com/DeepAgent-Architect/community-templates

# Once approved, template is available to all users
```

---

## Template Best Practices

1. **Clear Documentation** - Explain what template does
2. **Example Output** - Show expected results
3. **Parameter Validation** - Validate inputs
4. **Error Handling** - Graceful failures
5. **Cost Estimation** - Show expected cost
6. **Time Estimate** - How long it takes
7. **Prerequisites** - What's needed to run
8. **Customization Guide** - How to modify

---

## Workflow Execution

### Run Workflow

```bash
# Execute pre-built workflow
/workflow execute "weekly-intelligence"

# Execute with parameters
/workflow execute "due-diligence" \
  --company "Company X" \
  --investment_size 10000000 \
  --timeline "2 weeks"

# Schedule workflow
/workflow schedule "weekly-intelligence" \
  --cron "0 6 * * 1" \
  --timezone "America/New_York"
```

### Monitor Workflow

```bash
# Watch execution
/workflow monitor "weekly-intelligence" --watch

# Check status
/workflow status "weekly-intelligence"

# View results
/workflow results "weekly-intelligence" --latest
```

---

## Summary

**Community Templates provide:**
- ✅ Pre-built workflows
- ✅ Best practice patterns
- ✅ Time savings (80%+ faster)
- ✅ Cost optimization
- ✅ Knowledge sharing
- ✅ Continuous improvement

**Popular Categories:**
- Financial analysis
- Market research
- Problem-solving
- Monitoring
- Reporting
- Data pipelines

**Get Involved:**
- Use templates
- Share your templates
- Rate templates
- Contribute improvements
- Build on community work

---

**https://github.com/DeepAgent-Architect/community-templates**
