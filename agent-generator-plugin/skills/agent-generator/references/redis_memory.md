# Redis Memory Configuration

## Key Architecture

Redis stores agent memory using hierarchical keys: `namespace:agent_id:user_id:session_id:type`

### Key Structure
```
agent:memory:stock_analyzer:user_123:session_abc123:messages
agent:memory:stock_analyzer:user_123:profile:*
agent:memory:stock_analyzer:execution_cache:*
```

**Namespace**: `agent:memory`  
**Agent ID**: Identifies the agent type  
**User ID**: Isolates users' data  
**Session ID**: Conversation thread  
**Type**: `messages`, `profile`, `cache`, etc.

---

## Redis Integration with LangChain

### Basic Setup
```python
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
import redis

# Initialize Redis connection (with pooling)
pool = redis.ConnectionPool.from_url(
    "redis://localhost:6379/0",
    max_connections=10,
    decode_responses=True
)
redis_client = redis.Redis(connection_pool=pool)

# Create message history accessor
def get_agent_history(session_id: str, agent_id: str = "default"):
    return RedisChatMessageHistory(
        session_id=f"{agent_id}:{session_id}",
        url="redis://localhost:6379/0",
        key_prefix="agent:memory:",
        ttl=3600  # 1 hour session TTL
    )

# Wrap agent with history
wrapped_agent = RunnableWithMessageHistory(
    agent,
    get_session_history=get_agent_history,
    input_messages_key="messages",
    history_messages_key="history"
)

# Use with thread_id for persistence
result = wrapped_agent.invoke(
    {"messages": [{"role": "user", "content": "..."}]},
    config={"configurable": {"session_id": "user_123_session_abc"}}
)
```

---

## TTL Strategies

### Short-Term Memory (Conversation)
**TTL**: 300-3600 seconds (5 min - 1 hour)

```python
history = RedisChatMessageHistory(
    session_id=f"stock_agent:user_123:current_session",
    url="redis://localhost:6379/0",
    ttl=1800  # 30 minutes
)
```

Expires after inactivity, frees memory automatically.

### Long-Term Memory (User Profile)
**TTL**: None (persistent)

```python
# Store user preferences, trading history, etc.
profile_key = f"agent:profile:user_123"
redis_client.set(
    profile_key,
    json.dumps({
        "preferred_symbols": ["AAPL", "TSLA"],
        "alert_threshold": -0.3,
        "portfolio_size": 100000
    })
    # No TTL = persistent until manual deletion
)
```

### Sliding Window TTL
Refresh TTL on access to keep active sessions alive:

```python
def get_and_refresh(session_id: str, ttl: int = 3600):
    """Get session and refresh TTL."""
    history = RedisChatMessageHistory(
        session_id=session_id,
        url="redis://localhost:6379/0",
        ttl=ttl
    )
    # Access triggers automatic TTL reset in LangChain
    messages = history.messages
    return messages
```

---

## Connection Pooling & Retry Logic

### Production Configuration
```python
import redis
from redis.retry import Retry
from redis.backoff import ExponentialBackoff
from tenacity import retry, wait_exponential, stop_after_attempt

# Connection pool with backoff
pool = redis.ConnectionPool.from_url(
    "redis://localhost:6379/0",
    max_connections=10,
    retry=Retry(ExponentialBackoff(), 3),
    retry_on_timeout=True,
    socket_connect_timeout=5,
    socket_keepalive=True,
    health_check_interval=30
)

redis_client = redis.Redis(connection_pool=pool)

# Retry wrapper for Redis operations
@retry(
    wait=wait_exponential(multiplier=1, min=2, max=10),
    stop=stop_after_attempt(3)
)
def safe_redis_get(key: str) -> Optional[str]:
    """Get from Redis with automatic retry."""
    return redis_client.get(key)

@retry(
    wait=wait_exponential(multiplier=1, min=2, max=10),
    stop=stop_after_attempt(3)
)
def safe_redis_set(key: str, value: str, ttl: int = 3600):
    """Set in Redis with automatic retry."""
    return redis_client.set(key, value, ex=ttl)
```

### Dependency Installation
```bash
pip install redis tenacity python-dotenv
```

---

## Memory Operations

### Store Conversation History
```python
def save_conversation(
    agent_id: str,
    user_id: str,
    session_id: str,
    messages: list
):
    """Store messages in Redis."""
    history = RedisChatMessageHistory(
        session_id=f"{agent_id}:{user_id}:{session_id}",
        url="redis://localhost:6379/0",
        key_prefix="agent:memory:",
        ttl=3600
    )
    
    for msg in messages:
        if msg["role"] == "user":
            history.add_user_message(msg["content"])
        elif msg["role"] == "assistant":
            history.add_ai_message(msg["content"])
```

### Retrieve Conversation History
```python
def load_conversation(
    agent_id: str,
    user_id: str,
    session_id: str
) -> list:
    """Retrieve messages from Redis."""
    history = RedisChatMessageHistory(
        session_id=f"{agent_id}:{user_id}:{session_id}",
        url="redis://localhost:6379/0",
        key_prefix="agent:memory:"
    )
    return history.messages
```

### Store Custom Data (JSON)
```python
import json

def store_user_profile(user_id: str, profile: dict):
    """Store structured user data in Redis."""
    key = f"agent:profile:user:{user_id}"
    redis_client.set(
        key,
        json.dumps(profile),
        ex=None  # Persistent
    )

def load_user_profile(user_id: str) -> dict:
    """Load structured user data from Redis."""
    key = f"agent:profile:user:{user_id}"
    data = redis_client.get(key)
    return json.loads(data) if data else {}
```

### Clear Session
```python
def clear_session(agent_id: str, user_id: str, session_id: str):
    """Delete all session data from Redis."""
    pattern = f"agent:memory:{agent_id}:{user_id}:{session_id}*"
    for key in redis_client.scan_iter(match=pattern):
        redis_client.delete(key)
```

---

## Local Redis Setup (Docker)

For development:
```bash
# Run Redis in Docker
docker run -d \
  -p 6379:6379 \
  --name redis-agent \
  redis:7-alpine

# Or use docker-compose.yml
version: '3.8'
services:
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes
  
volumes:
  redis_data:
```

Test connection:
```bash
redis-cli ping
# Response: PONG
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `ConnectionError: Connection refused` | Ensure Redis is running (`docker ps`) |
| `WRONGTYPE Operation against a key holding the wrong kind of value` | Key has wrong type; use `redis-cli DEL key` to clear |
| `OOM command not allowed when used memory > 'maxmemory'` | Reduce TTL or increase Redis memory limit |
| `NOAUTH Authentication required` | Set `REDIS_PASSWORD` in env and use `redis://user:password@host:port/0` |
| Session data not persisting | Verify TTL is `None` for long-term memory; check Redis is not evicting keys |

---

## Monitoring

### Check Memory Usage
```bash
redis-cli INFO memory
# Returns: used_memory, used_memory_human, maxmemory, evicted_keys
```

### Monitor Active Sessions
```bash
# See all agent memory keys
redis-cli KEYS "agent:memory:*"

# Check specific session TTL
redis-cli TTL "agent:memory:stock_analyzer:user_123:session_abc"
```

### Clear Expired Keys
Redis automatically removes expired keys, but can force cleanup:
```bash
redis-cli FLUSHDB  # Clear all keys (use with caution!)
redis-cli FLUSHDB ASYNC  # Background cleanup
```
