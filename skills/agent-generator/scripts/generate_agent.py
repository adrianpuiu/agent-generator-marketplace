#!/usr/bin/env python3
"""
Agent Generation Orchestrator

Transforms natural language descriptions into production-ready LangGraph agents.
"""

import json
import re
from dataclasses import dataclass
from typing import Optional
from datetime import datetime

# Jinja2 template for agent generation
AGENT_TEMPLATE = '''#!/usr/bin/env python3
"""{{ agent_name }} - Generated {{ timestamp }}"""

import os
import sys
import logging
from typing import Optional
import asyncio

from langgraph.prebuilt import create_react_agent
{% if deep_agent %}from deepagents import create_deep_agent{% endif %}
from langchain_core.tools import tool
from pydantic import BaseModel, Field
{% if memory_backend == 'redis' %}
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
import redis
{% elif memory_backend == 'postgres' %}
from langgraph.checkpoint.postgres import PostgresSaver
{% else %}
from langgraph.checkpoint.memory import InMemorySaver
{% endif %}

# === Logging Configuration ===
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# === Tool Definitions ===
{% for tool in tools %}
class {{ tool['class_name'] }}(BaseModel):
{% for param in tool['parameters'] %}
    {{ param['name'] }}: {{ param['type'] }} = Field(
        {% if param['default'] %}default={{ param['default'] }}, {% endif %}
        description="{{ param['description'] }}"
    )
{% endfor %}

@tool(args_schema={{ tool['class_name'] }})
def {{ tool['func_name'] }}({{ tool['params_str'] }}) -> str:
    """{{ tool['description'] }}"""
    try:
        # Implementation placeholder - customize as needed
        logger.info(f"Tool called: {{ tool['func_name'] }} with args: {locals()}")
        return f"Result from {{ tool['func_name'] }}"
    except KeyError as e:
        logger.error(f"Missing API key: {e}")
        return f"Error: Set environment variable {str(e)}"
    except Exception as e:
        logger.error(f"Tool error: {type(e).__name__}: {e}")
        return f"Error: {str(e)}"

{% endfor %}

# === Memory Configuration ===
{% if memory_backend == 'redis' %}
def init_redis_memory(agent_id: str = "default"):
    """Initialize Redis connection pool and return history accessor."""
    try:
        pool = redis.ConnectionPool.from_url(
            os.getenv("REDIS_URL", "redis://localhost:6379/0"),
            max_connections=10,
            decode_responses=True
        )
        redis_client = redis.Redis(connection_pool=pool)
        redis_client.ping()
        logger.info("Redis connection established")
    except Exception as e:
        logger.error(f"Redis connection failed: {e}")
        logger.warning("Falling back to in-memory storage")
        return None

    def get_history(session_id: str):
        return RedisChatMessageHistory(
            session_id=f"{agent_id}:{session_id}",
            url=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
            key_prefix="agent:memory:",
            ttl=int(os.getenv("SESSION_TTL", 3600))
        )
    
    return get_history

memory_accessor = init_redis_memory()

{% elif memory_backend == 'postgres' %}
def init_postgres_memory():
    """Initialize PostgreSQL checkpointer."""
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise ValueError("DATABASE_URL not set for PostgreSQL memory")
    
    checkpointer = PostgresSaver.from_conn_string(db_url)
    logger.info("PostgreSQL checkpointer initialized")
    return checkpointer

checkpointer = init_postgres_memory()

{% else %}
from langgraph.checkpoint.memory import InMemorySaver
checkpointer = InMemorySaver()
logger.warning("Using in-memory checkpointer - state lost on restart")

{% endif %}

# === Agent Setup ===
tools = [
{% for tool in tools %}
    {{ tool['func_name'] }},
{% endfor %}
]

{% if deep_agent %}
agent = create_deep_agent(
    model="{{ model }}",
    tools=tools,
    system_prompt="""{{ system_prompt }}""",
)
{% else %}
agent = create_react_agent(
    model="{{ model }}",
    tools=tools,
    prompt="""{{ system_prompt }}"""
)
{% endif %}

{% if memory_backend == 'redis' and not deep_agent %}
if memory_accessor:
    agent_with_memory = RunnableWithMessageHistory(
        agent,
        get_session_history=memory_accessor,
        input_messages_key="messages",
        history_messages_key="history"
    )
else:
    agent_with_memory = agent
{% elif memory_backend != 'redis' and not deep_agent %}
app = agent.compile(checkpointer=checkpointer)
agent_with_memory = app
{% else %}
agent_with_memory = agent
{% endif %}

# === Main Execution ===
async def run_agent(user_input: str, session_id: str = "default"):
    """Run the agent with user input."""
    logger.info(f"Running agent with input: {user_input}")
    
    try:
        config = {"configurable": {"thread_id": session_id}} if session_id else {}
        
        result = await agent_with_memory.ainvoke(
            {"messages": [{"role": "user", "content": user_input}]},
            config=config
        )
        
        logger.info(f"Agent completed successfully")
        return result
    except Exception as e:
        logger.error(f"Agent execution failed: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    # Example usage
    import sys
    
    user_query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "{{ initial_query }}"
    session = os.getenv("SESSION_ID", "default_session")
    
    result = asyncio.run(run_agent(user_query, session_id=session))
    print(json.dumps(result, indent=2, default=str))
'''

@dataclass
class Tool:
    """Tool definition."""
    name: str
    description: str
    parameters: list[dict]  # [{"name": "...", "type": "...", "description": "..."}]
    
    @property
    def func_name(self) -> str:
        """Generate function name from tool name."""
        return self.name.lower().replace(" ", "_").replace("-", "_")
    
    @property
    def class_name(self) -> str:
        """Generate Pydantic class name."""
        return "".join(w.capitalize() for w in self.name.split()) + "Input"
    
    @property
    def params_str(self) -> str:
        """Generate parameter string for function signature."""
        params = []
        for p in self.parameters:
            default = f" = {p.get('default')}" if 'default' in p else ""
            params.append(f"{p['name']}: {p['type']}{default}")
        return ", ".join(params)

@dataclass
class AgentConfig:
    """Agent generation configuration."""
    name: str
    description: str
    tools: list[Tool]
    memory_backend: str = "memory"  # "memory", "redis", "postgres"
    model: str = "anthropic:claude-sonnet-4-20250514"
    deep_agent: bool = False
    system_prompt: str = "You are a helpful assistant."
    initial_query: str = "What can you help me with?"

def generate_agent_script(config: AgentConfig) -> str:
    """Generate agent script from configuration."""
    from jinja2 import Template
    
    template = Template(AGENT_TEMPLATE)
    
    context = {
        "agent_name": config.name.replace(" ", "_").lower(),
        "timestamp": datetime.now().isoformat(),
        "tools": [
            {
                "func_name": tool.func_name,
                "class_name": tool.class_name,
                "description": tool.description,
                "parameters": tool.parameters,
                "params_str": tool.params_str,
            }
            for tool in config.tools
        ],
        "memory_backend": config.memory_backend,
        "model": config.model,
        "deep_agent": config.deep_agent,
        "system_prompt": config.system_prompt,
        "initial_query": config.initial_query,
    }
    
    return template.render(context)

def extract_dependencies(script: str) -> list[str]:
    """Extract Python dependencies from generated script."""
    import_pattern = r"^(?:from|import)\s+(\S+)"
    imports = set()
    
    for line in script.split("\n"):
        match = re.match(import_pattern, line)
        if match:
            module = match.group(1).split(".")[0]
            imports.add(module)
    
    # Map to package names
    mapping = {
        "langgraph": "langgraph>=0.1.0",
        "langchain": "langchain>=0.3.0",
        "langchain_core": "langchain-core>=0.3.0",
        "langchain_community": "langchain-community>=0.3.0",
        "pydantic": "pydantic>=2.0.0",
        "deepagents": "deepagents>=0.2.7",
        "redis": "redis>=5.0.0",
    }
    
    requirements = []
    for imp in sorted(imports):
        if imp in mapping:
            requirements.append(mapping[imp])
    
    return requirements

if __name__ == "__main__":
    # Example: Generate stock sentiment agent
    example_config = AgentConfig(
        name="Stock Sentiment Analyzer",
        description="Analyzes stock sentiment from news",
        tools=[
            Tool(
                name="Get Stock Sentiment",
                description="Get market sentiment score for a stock",
                parameters=[
                    {
                        "name": "symbol",
                        "type": "str",
                        "description": "Stock ticker symbol (e.g., AAPL)"
                    }
                ]
            ),
            Tool(
                name="Get Stock Price",
                description="Get real-time stock price",
                parameters=[
                    {
                        "name": "symbol",
                        "type": "str",
                        "description": "Stock ticker symbol"
                    }
                ]
            )
        ],
        memory_backend="redis",
        system_prompt="You are a stock analysis expert. Analyze sentiment and price trends.",
    )
    
    script = generate_agent_script(example_config)
    deps = extract_dependencies(script)
    
    print("=== GENERATED SCRIPT ===")
    print(script)
    print("\n=== REQUIREMENTS.TXT ===")
    for dep in deps:
        print(dep)
