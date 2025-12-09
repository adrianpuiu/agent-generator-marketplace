# Integration Guide

Complete reference for integrating agents with external services.

## Integration Architecture

```
┌─────────────────┐
│  Generated      │
│  Agent          │
└────────┬────────┘
         │
    ┌────▼─────────────────────────┐
    │  Integration Framework       │
    ├──────────────────────────────┤
    │ ├─ GitHub Connector         │
    │ ├─ Slack Connector          │
    │ ├─ Webhook Connector        │
    │ ├─ Email Connector          │
    │ ├─ Database Connector       │
    │ └─ Monitoring Connector     │
    └────┬──────────────────────────┘
         │
    ┌────┴──────────┬─────────┬────────┬─────────┬──────────┐
    │               │         │        │         │          │
   GitHub        Slack    Webhooks   Email   Database   Monitoring
```

## Quick Start Configurations

### GitHub Integration

```python
# config/github_config.py
GITHUB_CONFIG = {
    "owner": "company",
    "repo": "analysis-results",
    "branch": "main",
    "folder": "reports",
    "auto_commit": True,
    "create_pr": True,
    "pr_template": "Agent analysis: {topic}",
    "labels": ["agent-generated"],
    "auth_method": "token",  # or "app", "oauth"
}
```

### Slack Integration

```python
# config/slack_config.py
SLACK_CONFIG = {
    "webhook_url": os.getenv("SLACK_WEBHOOK_URL"),
    "channel": "#analysis",
    "format": "summary",  # or "detailed", "compact"
    "thread_replies": True,
    "mentions": ["@research-team"],
    "include_attachments": True,
    "progress_updates": True,
}
```

### Webhook Integration

```python
# config/webhook_config.py
WEBHOOK_CONFIG = {
    "url": os.getenv("WEBHOOK_URL"),
    "method": "POST",
    "headers": {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('WEBHOOK_TOKEN')}",
    },
    "retry_strategy": {
        "max_retries": 3,
        "backoff_factor": 2,
        "timeout": 30,
    },
}
```

## Integration Patterns

### Pattern 1: Results Publishing

Publish agent results to central repository:

```python
class PublishingIntegration:
    async def publish_results(self, agent_output):
        # 1. Format output
        formatted = self.format_for_publishing(agent_output)
        
        # 2. Commit to GitHub
        await self.github_connector.commit(
            files=formatted,
            message=f"Analysis: {agent_output['topic']}"
        )
        
        # 3. Create PR
        pr = await self.github_connector.create_pr(
            title=f"Analysis: {agent_output['topic']}",
            description=agent_output['summary']
        )
        
        # 4. Notify in Slack
        await self.slack_connector.post(
            channel="#analysis",
            text=f"New analysis published:\n{pr['html_url']}"
        )
```

### Pattern 2: Real-Time Notifications

Notify team of progress and results:

```python
class NotificationIntegration:
    async def notify_progress(self, agent_id, iteration, total):
        progress = (iteration / total) * 100
        
        if progress % 25 == 0:  # Every 25%
            await self.slack_connector.post(
                channel="#analysis",
                text=f"Agent {agent_id}: {progress:.0f}% complete"
            )
    
    async def notify_completion(self, agent_output):
        await self.slack_connector.post(
            channel="#analysis",
            text=f"Agent completed: {agent_output['title']}",
            attachments=[{
                "title": "View Results",
                "text": agent_output['summary'],
                "actions": [{"type": "button", "url": agent_output['link']}]
            }]
        )
```

### Pattern 3: Data Pipeline

Feed results into downstream systems:

```python
class DataPipelineIntegration:
    async def feed_results(self, agent_output):
        # 1. Transform results
        data = self.transform_for_pipeline(agent_output)
        
        # 2. Store in database
        await self.database_connector.insert(
            table="agent_results",
            data=data
        )
        
        # 3. Trigger downstream processing
        await self.webhook_connector.post(
            url=os.getenv("DOWNSTREAM_WEBHOOK"),
            data={"result_id": data['id']}
        )
        
        # 4. Update monitoring
        await self.monitoring_connector.record_event(
            event_type="result_published",
            agent_id=agent_output['agent_id'],
            result_id=data['id']
        )
```

## Service-Specific Configuration

### GitHub Actions CI/CD

Trigger agent runs via GitHub Actions:

```yaml
# .github/workflows/agent-research.yml
name: Weekly Market Research

on:
  schedule:
    - cron: '0 9 * * 1'  # Monday 9 AM

jobs:
  research:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Run Market Research Agent
        run: |
          /research-agent "Weekly market analysis" \
            --preset thorough \
            --memory redis \
            --integrate github
      
      - name: Commit results
        run: |
          git config user.name "Research Bot"
          git config user.email "bot@company.com"
          git add reports/
          git commit -m "Weekly market research results"
          git push
```

### Slack Workflow Builder

Trigger agents from Slack:

```
1. Slack user types in channel: "/research quantum companies"
2. Slack Workflow:
   - Extract topic: "quantum companies"
   - POST to webhook: {topic: "quantum companies"}
3. Your system:
   - Receives webhook
   - Triggers /research-agent "quantum companies"
   - Watches for completion
4. On completion:
   - POST results back to Slack
   - Post in same thread
```

### Cloud Scheduler (Google Cloud)

Automated scheduled execution:

```yaml
# cloud-scheduler-config.yaml
name: daily-stock-analysis
schedule: "30 9 * * 1-5"  # Weekdays 9:30 AM
timezone: "America/New_York"

httpTarget:
  uri: "https://your-api.com/agents/execute"
  httpMethod: POST
  oidcToken:
    serviceAccountEmail: "agent-runner@project.iam.gserviceaccount.com"
  body:
    agentType: "multi-agent-team"
    config:
      numAgents: 10
      task: "Monitor 100 stocks"
      integrations:
        - slack
        - monitoring
```

## Error Handling & Retries

```python
class IntegrationErrorHandler:
    async def execute_with_retry(self, integration_fn, max_retries=3):
        for attempt in range(max_retries):
            try:
                return await integration_fn()
            
            except IntegrationConnectionError as e:
                if attempt < max_retries - 1:
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
                    continue
                raise
            
            except IntegrationAuthError as e:
                # Auth errors should not retry
                await self.slack_connector.post_error(str(e))
                raise
            
            except IntegrationQuotaError as e:
                # Quota exceeded, wait longer
                await asyncio.sleep(300)
                continue
```

## Testing Integrations

```python
# tests/test_integrations.py

async def test_github_integration():
    """Test GitHub integration"""
    config = GITHUB_CONFIG.copy()
    connector = GitHubConnector(config)
    
    # Test connection
    assert await connector.test_connection()
    
    # Test commit
    result = await connector.commit(
        files={"test.md": "test content"},
        message="Test commit"
    )
    assert result['status'] == 'success'

async def test_slack_integration():
    """Test Slack integration"""
    config = SLACK_CONFIG.copy()
    connector = SlackConnector(config)
    
    # Test webhook
    result = await connector.post(
        channel="#test",
        text="Test message"
    )
    assert result['status'] == 'sent'

async def test_integration_chain():
    """Test full integration chain"""
    agent_output = {"topic": "test", "summary": "test summary"}
    
    # Publish to GitHub
    await github_connector.commit(...)
    
    # Post to Slack
    await slack_connector.post(...)
    
    # Store in database
    await database_connector.insert(...)
    
    # Verify all completed
    assert all_integrations_successful()
```

## Monitoring Integration Health

```python
class IntegrationMonitoring:
    async def check_health(self):
        health_status = {}
        
        # Check each integration
        health_status['github'] = await self.check_github()
        health_status['slack'] = await self.check_slack()
        health_status['database'] = await self.check_database()
        health_status['webhooks'] = await self.check_webhooks()
        
        return health_status
    
    async def check_github(self):
        try:
            response = await self.github_connector.test_connection()
            return {"status": "healthy", "latency_ms": response['latency']}
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}
```

## Cost Optimization

Reduce integration costs:

```python
# batch_results.py - Reduce API calls
class BatchIntegration:
    def __init__(self, batch_size=5, batch_timeout=60):
        self.batch_size = batch_size
        self.batch_timeout = batch_timeout
        self.pending_posts = []
    
    async def post_event(self, event):
        self.pending_posts.append(event)
        
        if len(self.pending_posts) >= self.batch_size:
            await self.flush()
    
    async def flush(self):
        if self.pending_posts:
            # Single API call for multiple events
            await self.slack_connector.post_batch(self.pending_posts)
            self.pending_posts = []
```

## Summary

**Integrations connect agents to:**
- ✅ Version control (GitHub)
- ✅ Communication (Slack)
- ✅ Custom systems (Webhooks)
- ✅ Data storage (Databases)
- ✅ Monitoring (Datadog, CloudWatch)
- ✅ Scheduling (Cloud Scheduler)
- ✅ CI/CD (GitHub Actions)

**Benefits:**
- Automated workflows
- Team visibility
- Data persistence
- System integration
- Enterprise automation
