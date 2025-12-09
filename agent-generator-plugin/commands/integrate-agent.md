---
description: Integrate generated agents with external services - GitHub, Slack, databases, webhooks, and monitoring
argument-hint: "[integration type] [configuration]"
---

# Integrate Agent

Connect your generated agents with external services and workflows for automated execution, reporting, and collaboration.

## Supported Integrations

### 1. GitHub Integration
Commit agent outputs directly to your repository.

```bash
/integrate-agent github \
  --repo "github.com/yourname/research" \
  --branch "main" \
  --folder "reports" \
  --auth-token $GITHUB_TOKEN
```

**Features:**
- Auto-commit analysis results
- Create pull requests for review
- Version control for all outputs
- CI/CD integration ready

**Workflow:**
```
Agent generates analysis
   ↓
Commits to GitHub repo
   ↓
Creates PR for review
   ↓
Auto-merge on approval
```

---

### 2. Slack Integration
Send agent results to Slack channels automatically.

```bash
/integrate-agent slack \
  --webhook-url "https://hooks.slack.com/..." \
  --channel "#research" \
  --format "summary"
```

**Features:**
- Post results to channels
- Thread discussions
- @mentions for attention
- Rich formatting

**Real Example:**
```
Agent completes market research
   ↓
Posts summary to #research
   ↓
Attaches full report
   ↓
Mentions @strategy-team
   ↓
Team reviews and discusses
```

---

### 3. Webhook Integration
Send results to any HTTP endpoint.

```bash
/integrate-agent webhook \
  --url "https://yourapi.com/agent-results" \
  --method POST \
  --auth-type bearer \
  --auth-token $API_TOKEN
```

**Use Cases:**
- Custom dashboards
- Data warehouses
- External analytics
- Custom workflows

---

### 4. Email Integration
Automatically email reports to stakeholders.

```bash
/integrate-agent email \
  --recipients "team@company.com" \
  --subject-template "Market Research: {topic}" \
  --format "html"
```

**Features:**
- Scheduled emails
- Recipient lists
- HTML formatting
- Attachment support

---

### 5. Database Integration
Store results in your database.

```bash
/integrate-agent database \
  --type "postgres" \
  --connection-string "postgresql://..." \
  --table "agent_results" \
  --schema "analysis"
```

**Supported:**
- PostgreSQL
- MySQL
- MongoDB
- DynamoDB

---

### 6. Monitoring Integration
Track agent performance and results.

```bash
/integrate-agent monitoring \
  --service "datadog" \
  --api-key $DATADOG_KEY \
  --tag-results yes
```

**Supported Services:**
- Datadog
- New Relic
- CloudWatch
- Prometheus

---

## Configuration Examples

### Example 1: Complete CI/CD Pipeline

```bash
# Generate research agent
/research-agent "Quarterly market analysis" \
  --integrate github,slack,database \
  --auto-trigger "schedule:weekly:monday:09:00"

# Workflow:
# 1. Scheduled trigger (Monday 9 AM)
# 2. Agent runs research
# 3. Results committed to GitHub
# 4. PR created for review
# 5. On approval, merged to main
# 6. Slack notification sent
# 7. Results stored in database
```

---

### Example 2: Team Collaboration Setup

```bash
# Multi-agent analysis with integrations
/multi-agent-team "Analyze 50 companies" \
  --num-agents 10 \
  --integrate slack,monitoring,database \
  --slack-channel "#analysis" \
  --slack-updates "progress,summary" \
  --datadog-dashboard "analysis-metrics"

# Workflow:
# 1. Coordinator plans (Slack: "Starting analysis")
# 2. Workers execute (Datadog: Progress metrics)
# 3. Each worker completes (Slack: Progress update)
# 4. Results aggregated
# 5. Database: Final results stored
# 6. Slack: Summary posted with @mentions
# 7. Monitoring: Performance metrics tracked
```

---

### Example 3: Automated Daily Reporting

```bash
# Analysis with automatic daily reporting
/analysis-agent "Market metrics daily" \
  --integrate email,slack,webhook \
  --schedule "daily:06:00" \
  --email-recipients "executives@company.com" \
  --slack-channel "#daily-metrics" \
  --webhook-url "https://dashboard.company.com/metrics"

# Workflow:
# 1. Daily 6 AM trigger
# 2. Agent analyzes latest data
# 3. Email sent to executives
# 4. Slack post to #daily-metrics
# 5. Webhook updates dashboard
# 6. All automated, no manual work
```

---

## Integration Reference

### GitHub Integration Options
```yaml
github:
  repo: "owner/repo"
  branch: "main"
  folder: "reports"
  commit_message: "Agent: {topic}"
  create_pr: true
  auto_merge: false
  labels: ["agent-generated", "review-needed"]
  assignees: ["team-lead"]
```

### Slack Integration Options
```yaml
slack:
  webhook_url: "https://hooks.slack.com/..."
  channel: "#research"
  format: "summary"  # or "detailed", "compact"
  thread_replies: true
  mentions: ["@research-team"]
  include_attachments: true
  include_links: true
```

### Webhook Integration Options
```yaml
webhook:
  url: "https://api.company.com/results"
  method: "POST"
  headers:
    Content-Type: "application/json"
    Authorization: "Bearer {token}"
  payload_format: "standard"  # or "custom"
  retry_count: 3
  timeout: 30
```

### Database Integration Options
```yaml
database:
  type: "postgres"
  connection: "postgresql://..."
  table: "agent_results"
  schema: "public"
  auto_create_table: true
  fields:
    - agent_type
    - task_description
    - results
    - timestamp
    - metadata
```

### Email Integration Options
```yaml
email:
  provider: "sendgrid"  # or "aws-ses", "smtp"
  recipients: ["team@company.com"]
  subject: "Agent Results: {topic}"
  format: "html"  # or "markdown", "text"
  include_attachments: true
  schedule: "on_completion"  # or "daily:09:00"
```

---

## Real-World Integration Scenarios

### Scenario 1: Investment Research Workflow

```bash
# Complete automated research → review → publish workflow

# 1. Generate analysis agent
/research-agent "SaaS IPO candidates Q1 2025" \
  --preset thorough \
  --integrate github,slack \
  --github-repo "company/investment-research" \
  --github-branch "analysis" \
  --slack-channel "#investments"

# 2. Agent runs (15-20 minutes)
#    - Plans research
#    - Searches for candidates
#    - Analyzes funding/metrics
#    - Generates investment thesis

# 3. GitHub automatically:
#    - Commits analysis.md
#    - Commits findings.json
#    - Creates PR for review
#    - Tags @investments-team

# 4. Slack automatically:
#    - Posts summary
#    - Mentions @investments-team
#    - Provides review link

# 5. Team reviews PR:
#    - Comments on findings
#    - Requests changes
#    - Approves

# 6. On approval:
#    - PR auto-merges to main
#    - Slack: "Analysis published"
#    - Email sent to stakeholders

# Time: 30 minutes (automated)
```

---

### Scenario 2: Continuous Monitoring & Alerts

```bash
# Automated daily market analysis with alerts

/multi-agent-team "Monitor 100 stocks" \
  --num-agents 10 \
  --integrate monitoring,slack,webhook \
  --schedule "daily:09:30" \
  --datadog-dashboard "stock-monitoring" \
  --slack-channel "#trading" \
  --webhook-url "https://trading-system.company.com/signals"

# Workflow:
# 1. Daily 9:30 AM (market open)
# 2. 10 agents analyze stocks in parallel
# 3. Results stream to monitoring:
#    - Datadog: Real-time metrics
#    - Performance tracking
# 4. Slack updates:
#    - Every 5 minutes: Agent progress
#    - Anomalies detected: Immediate alert
#    - Final summary: All findings
# 5. Webhook:
#    - Signal trade opportunities
#    - Feed into trading system
#    - Auto-execute if criteria met

# Time: 25 minutes (fully automated)
```

---

### Scenario 3: Team Collaboration & Review

```bash
# Collaborative analysis with full team engagement

/multi-agent-team "Analyze competitor" \
  --num-agents 5 \
  --specialist-roles "tech,market,financial,team,competitive" \
  --integrate github,slack,database \
  --github-repo "company/competitive-analysis" \
  --slack-channel "#strategy" \
  --database "postgres" \
  --assign-for-review "@strategy-team"

# Workflow:
# 1. Coordinator creates work plan
#    - Slack: "Analysis starting"
# 2. 5 specialists analyze in parallel
#    - Each posts intermediate findings
#    - Questions answered in thread
# 3. Results aggregated
#    - All findings combined
#    - Slack: Summary with @mentions
# 4. Committed to GitHub
#    - Pull request created
#    - @strategy-team assigned
#    - Code review style feedback
# 5. Stored in database
#    - Queryable findings
#    - Historical comparison
#    - Trend analysis

# Team collaboration: Slack discussion + GitHub review
```

---

## Best Practices

1. **Start Simple** - One integration first
2. **Test Locally** - Verify before scheduling
3. **Use Environments** - Dev/test/prod
4. **Monitor Runs** - Track success/failure
5. **Version Control** - Keep analysis history
6. **Secure Tokens** - Use environment variables
7. **Document Workflows** - For team knowledge
8. **Set Alerts** - For failures

---

## Integration Troubleshooting

**GitHub integration failing:**
→ Check token permissions (repo, workflow)
→ Verify branch exists
→ Check folder exists

**Slack integration not sending:**
→ Verify webhook URL
→ Check channel name
→ Verify bot permissions

**Database connection error:**
→ Test connection string
→ Verify table exists or auto-create enabled
→ Check credentials

**Monitoring not tracking:**
→ Verify API key
→ Check service availability
→ Review metric names

---

## Cost Considerations

**Free Tier Services:**
- GitHub (unlimited commits)
- Slack (message limits)
- Webhooks (your own infrastructure)

**Paid Services:**
- Datadog: $15-30/mo
- New Relic: $20-50/mo
- Email: $10-20/mo (for volume)

**Budget Estimate:**
- Small team (1-5 agents): $0-30/mo
- Medium team (5-20 agents): $30-100/mo
- Large team (20+ agents): $100+/mo

---

## Advanced: Custom Integrations

Users can implement custom integrations:

```python
# In generated_agent.py

class CustomIntegration:
    async def on_agent_complete(self, results):
        # Custom logic
        await self.post_to_internal_system(results)
        await self.update_custom_dashboard(results)
        await self.notify_custom_channels(results)
```

---

## Summary

**Integrations enable:**
- ✅ Automated workflows
- ✅ Team collaboration
- ✅ Continuous monitoring
- ✅ Historical tracking
- ✅ External system connectivity
- ✅ Enterprise automation

**Supported Services:**
- GitHub (version control)
- Slack (team communication)
- Webhooks (custom integrations)
- Email (distribution)
- Databases (persistence)
- Monitoring (observability)

**Next Step:** Configure your first integration!
