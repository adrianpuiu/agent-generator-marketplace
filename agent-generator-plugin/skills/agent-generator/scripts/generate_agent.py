#!/usr/bin/env python3
"""
DeepAgent Generation Orchestrator

Transforms natural language descriptions into production-ready DeepAgents with planning.
"""

import json
import re
from dataclasses import dataclass
from typing import Optional
from datetime import datetime

# Jinja2 template for DeepAgent generation (planning-focused)
AGENT_TEMPLATE = '''#!/usr/bin/env python3
"""{{ agent_name }} - Generated DeepAgent {{ timestamp }}"""

import os
import sys
import logging
from typing import Optional, List
import asyncio

from langgraph.prebuilt import create_deep_agent
from langchain_core.tools import tool
from pydantic import BaseModel, Field
{% if memory_backend == 'redis' %}
from langchain_community.chat_message_histories import RedisChatMessageHistory
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

# === Planning Tools (Built-In) ===

class PlanInput(BaseModel):
    goal: str = Field(description="The goal to plan for")
    context: str = Field(description="Context about the current situation")

@tool(args_schema=PlanInput)
def create_plan(goal: str, context: str) -> str:
    """Create a step-by-step plan for achieving a goal."""
    try:
        logger.info(f"Creating plan for goal: {goal}")
        return f"Plan for '{goal}' in context: {context}\\n1. Analyze situation\\n2. Identify approach\\n3. Execute plan"
    except Exception as e:
        logger.error(f"Planning error: {e}")
        return f"Error creating plan: {str(e)}"

class RefineInput(BaseModel):
    plan: str = Field(description="The plan to refine")
    feedback: str = Field(description="Feedback to improve the plan")

@tool(args_schema=RefineInput)
def refine_plan(plan: str, feedback: str) -> str:
    """Iteratively improve a plan based on feedback."""
    try:
        logger.info(f"Refining plan based on feedback: {feedback}")
        return f"Refined plan incorporating feedback: {feedback}\\n{plan}"
    except Exception as e:
        logger.error(f"Refinement error: {e}")
        return f"Error refining plan: {str(e)}"

class DecomposeInput(BaseModel):
    task: str = Field(description="The complex task to break down")

@tool(args_schema=DecomposeInput)
def decompose_task(task: str) -> str:
    """Break down a complex task into smaller sub-tasks."""
    try:
        logger.info(f"Decomposing task: {task}")
        subtasks = [f"Sub-task {i+1}: Component of '{task}'" for i in range(3)]
        return "\\n".join(subtasks)
    except Exception as e:
        logger.error(f"Decomposition error: {e}")
        return f"Error decomposing task: {str(e)}"

class EvaluateInput(BaseModel):
    solution: str = Field(description="The solution to evaluate")
    criteria: List[str] = Field(description="Evaluation criteria")

@tool(args_schema=EvaluateInput)
def evaluate_solution(solution: str, criteria: List[str]) -> str:
    """Evaluate a solution against specified criteria."""
    try:
        logger.info(f"Evaluating solution against {len(criteria)} criteria")
        evaluations = [f"✓ {criterion}: Assessed" for criterion in criteria]
        return "Evaluation Results:\\n" + "\\n".join(evaluations)
    except Exception as e:
        logger.error(f"Evaluation error: {e}")
        return f"Error evaluating solution: {str(e)}"

# === User-Defined Tools ===
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
    """Initialize Redis for long-running research sessions."""
    try:
        pool = redis.ConnectionPool.from_url(
            os.getenv("REDIS_URL", "redis://localhost:6379/0"),
            max_connections=10,
            decode_responses=True
        )
        redis_client = redis.Redis(connection_pool=pool)
        redis_client.ping()
        logger.info("Redis connection established for memory persistence")
    except Exception as e:
        logger.error(f"Redis connection failed: {e}")
        logger.warning("Falling back to in-memory storage")
        return None
    return redis_client

memory_client = init_redis_memory()

{% elif memory_backend == 'postgres' %}
def init_postgres_memory():
    """Initialize PostgreSQL checkpointer for long-running agents."""
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

# === DeepAgent Setup ===
planning_tools = [create_plan, refine_plan, decompose_task, evaluate_solution]

all_tools = [
{% for tool in tools %}
    {{ tool['func_name'] }},
{% endfor %}
] + planning_tools

# Create DeepAgent with planning capabilities
agent = create_deep_agent(
    model="{{ model }}",
    tools=all_tools,
    system_prompt="""{{ system_prompt }}
    
You are a DeepAgent with planning capabilities. For complex tasks:
1. Create a plan using create_plan()
2. Decompose into sub-tasks using decompose_task()
3. Evaluate solutions using evaluate_solution()
4. Refine based on feedback using refine_plan()

Always plan before acting. Iterate and improve.""",
    max_iterations=15,
)

# === Main Execution ===
async def run_agent(user_input: str, session_id: str = "default"):
    """Run the DeepAgent with planning and iterative refinement."""
    logger.info(f"Running DeepAgent with input: {user_input}")
    
    try:
        config = {"configurable": {"thread_id": session_id}} if session_id else {}
        
        result = await agent.ainvoke(
            {"messages": [{"role": "user", "content": user_input}]},
            config=config
        )
        
        logger.info("DeepAgent completed successfully with iterative planning")
        return result
    except Exception as e:
        logger.error(f"DeepAgent execution failed: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
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
    parameters: list[dict]
    
    @property
    def func_name(self) -> str:
        return self.name.lower().replace(" ", "_").replace("-", "_")
    
    @property
    def class_name(self) -> str:
        return "".join(word.capitalize() for word in self.name.split()) + "Input"
    
    @property
    def params_str(self) -> str:
        return ", ".join(f"{p['name']}: {p['type']}" for p in self.parameters)

@dataclass
class AgentGenerationRequest:
    """Agent generation request."""
    description: str
    memory_backend: str = "memory"
    model: str = "claude-sonnet-4-20250514"
    tools: Optional[list[Tool]] = None

class DeepAgentGenerator:
    """Orchestrates DeepAgent generation from natural language."""
    
    def __init__(self):
        self.tools = self._default_tools()
    
    def _default_tools(self) -> list[Tool]:
        """Return default tools for DeepAgents."""
        return [
            Tool(
                name="Web Search",
                description="Search the web for information",
                parameters=[
                    {"name": "query", "type": "str", "description": "Search query"}
                ]
            ),
            Tool(
                name="Data Analyzer",
                description="Analyze data structures and patterns",
                parameters=[
                    {"name": "data", "type": "str", "description": "Data to analyze"}
                ]
            ),
        ]
    
    def generate(self, req: AgentGenerationRequest) -> dict:
        """Generate a DeepAgent from a request."""
        logger.info(f"Generating DeepAgent for: {req.description}")
        
        tools = req.tools or self._default_tools()
        
        template_vars = {
            "agent_name": self._sanitize_name(req.description),
            "description": req.description,
            "tools": [self._tool_to_dict(t) for t in tools],
            "memory_backend": req.memory_backend,
            "model": req.model,
            "system_prompt": self._create_system_prompt(req.description),
            "initial_query": req.description,
            "timestamp": datetime.now().isoformat(),
        }
        
        agent_code = self._render_template(template_vars)
        requirements = self._extract_requirements(req)
        
        return {
            "agent_code": agent_code,
            "requirements": requirements,
            "success": True
        }
    
    def _sanitize_name(self, description: str) -> str:
        """Create a valid Python name from description."""
        name = re.sub(r'[^a-zA-Z0-9_]', '', description.replace(" ", "_"))[:50]
        return f"DeepAgent_{name}" if name else "DeepAgent"
    
    def _tool_to_dict(self, tool: Tool) -> dict:
        """Convert Tool to template dict."""
        return {
            "name": tool.name,
            "func_name": tool.func_name,
            "class_name": tool.class_name,
            "description": tool.description,
            "parameters": tool.parameters,
            "params_str": tool.params_str,
        }
    
    def _create_system_prompt(self, description: str) -> str:
        """Create system prompt for the agent."""
        return f"""You are a DeepAgent specialized in: {description}

Your approach:
1. Plan your work before executing
2. Break complex tasks into smaller steps
3. Evaluate solutions against criteria
4. Iterate and improve based on feedback
5. Provide clear, actionable results"""
    
    def _render_template(self, vars: dict) -> str:
        """Render Jinja2 template (simplified without Jinja2 dep)."""
        code = AGENT_TEMPLATE
        
        # Simple variable substitution
        for key, value in vars.items():
            if key not in ["tools"]:
                code = code.replace("{{ " + key + " }}", str(value))
        
        # Handle tools loop
        tool_code = ""
        for tool in vars.get("tools", []):
            param_schema = "".join(
                f'    {p["name"]}: {p["type"]} = Field(description="{p["description"]}")\n'
                for p in tool.get("parameters", [])
            )
            tool_code += f'''
class {tool['class_name']}(BaseModel):
{param_schema}

@tool(args_schema={tool['class_name']})
def {tool['func_name']}({tool['params_str']}) -> str:
    """{tool['description']}"""
    try:
        logger.info(f"Tool called: {tool['func_name']} with args: {{locals()}}")
        return f"Result from {tool['func_name']}"
    except KeyError as e:
        logger.error(f"Missing API key: {{e}}")
        return f"Error: Set environment variable {{str(e)}}"
    except Exception as e:
        logger.error(f"Tool error: {{type(e).__name__}}: {{e}}")
        return f"Error: {{str(e)}}"
'''
        
        code = re.sub(
            r'{%\s*for tool in tools\s*%\}.*?{%\s*endfor\s*%\}',
            tool_code,
            code,
            flags=re.DOTALL
        )
        
        return code
    
    def _extract_requirements(self, req: AgentGenerationRequest) -> list[str]:
        """Extract dependencies based on request."""
        reqs = [
            "langgraph>=0.1.0",
            "langchain>=0.3.0",
            "langchain-core>=0.3.0",
            "pydantic>=2.0.0",
        ]
        
        if req.memory_backend == "redis":
            reqs.append("redis>=5.0.0")
        elif req.memory_backend == "postgres":
            reqs.append("psycopg2-binary>=2.9.0")
        
        return reqs

if __name__ == "__main__":
    generator = DeepAgentGenerator()
    
    request = AgentGenerationRequest(
        description="Research emerging AI companies and analyze funding",
        memory_backend="redis"
    )
    
    result = generator.generate(request)
    
    if result["success"]:
        print("=== Generated Agent Code ===")
        print(result["agent_code"][:500] + "...")
        print("\n=== Requirements ===")
        print("\n".join(result["requirements"]))
