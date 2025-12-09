#!/usr/bin/env python3
"""
Multi-Agent Team Template - Coordinator spawns specialist workers for parallel processing

Generated from /multi-agent-team command
"""

import os
import sys
import logging
from typing import Optional, List
import asyncio
import json
from dataclasses import dataclass

from langgraph.prebuilt import create_deep_agent
from langchain_core.tools import tool
from pydantic import BaseModel, Field

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# === Coordinator Tools ===

class WorkPlanInput(BaseModel):
    task: str = Field(description="Large task to distribute")
    num_workers: int = Field(description="Number of workers to create")

@tool(args_schema=WorkPlanInput)
def plan_work_distribution(task: str, num_workers: int) -> str:
    """Plan how to distribute work among workers."""
    logger.info(f"Planning work distribution for {num_workers} workers")
    plan = f"""
Work Distribution Plan:
Task: {task}
Workers: {num_workers}

Distribution Strategy:
1. Divide work into {num_workers} batches
2. Assign each batch to a worker
3. Workers execute in parallel
4. Collect results as they complete
5. Aggregate findings

[Detailed work breakdown would be generated]
"""
    return plan

@tool
def spawn_worker_agents(num_workers: int = 5) -> str:
    """Spawn N specialist worker agents."""
    logger.info(f"Spawning {num_workers} worker agents")
    agents = [f"Worker_{i+1}" for i in range(num_workers)]
    return f"Spawned workers: {agents}"

# === Aggregator Tools ===

class AggregateInput(BaseModel):
    worker_results: List[str] = Field(description="Results from each worker")

@tool(args_schema=AggregateInput)
def aggregate_results(worker_results: List[str]) -> str:
    """Combine results from multiple workers."""
    logger.info(f"Aggregating {len(worker_results)} worker results")
    return f"Aggregated Results:\n[Unified findings from all workers]"

@tool
def identify_patterns() -> str:
    """Find patterns across all worker results."""
    return "Cross-Worker Patterns:\n[Patterns identified from aggregated results]"

@tool
def generate_alerts() -> str:
    """Generate alerts for high-priority findings."""
    return "Alerts:\n[High-priority items flagged for attention]"

@tool
def create_summary_report() -> str:
    """Create executive summary of findings."""
    return "Summary Report:\n[Executive overview of all findings]"

# === Coordinator Agent ===

coordinator_tools = [
    plan_work_distribution,
    spawn_worker_agents,
]

coordinator = create_deep_agent(
    model="claude-sonnet-4-20250514",
    tools=coordinator_tools,
    system_prompt="""You are a Coordinator DeepAgent managing a team of specialist workers.

Your approach:
1. Plan work distribution for the task
2. Spawn N specialist worker agents
3. Delegate tasks to workers
4. Track worker progress
5. Collect results as they complete
6. Coordinate with aggregator

Always:
- Plan work clearly
- Balance load across workers
- Monitor progress
- Handle worker failures
- Coordinate handoff to aggregator
""",
    max_iterations=10,
)

# === Aggregator Agent ===

aggregator_tools = [
    aggregate_results,
    identify_patterns,
    generate_alerts,
    create_summary_report,
]

aggregator = create_deep_agent(
    model="claude-sonnet-4-20250514",
    tools=aggregator_tools,
    system_prompt="""You are an Aggregator DeepAgent combining results from specialist workers.

Your approach:
1. Receive results from all workers
2. Combine and deduplicate
3. Identify cross-worker patterns
4. Flag high-priority findings
5. Generate unified report
6. Create executive summary

Always:
- Validate data quality
- Find patterns across sources
- Resolve conflicts in findings
- Highlight anomalies
- Generate actionable insights
""",
    max_iterations=10,
)

class MultiAgentTeam:
    """Orchestrates multi-agent parallel processing."""
    
    def __init__(self, num_workers: int = 5):
        self.num_workers = num_workers
        self.coordinator = coordinator
        self.aggregator = aggregator
        logger.info(f"Initialized multi-agent team with {num_workers} workers")
    
    async def run(self, task: str, items: List[str], session_id: str = "default"):
        """Run the multi-agent team."""
        logger.info(f"Starting multi-agent processing: {task}")
        
        try:
            # 1. Coordinator plans work
            config = {"configurable": {"thread_id": f"{session_id}_coordinator"}}
            plan_result = await coordinator.ainvoke(
                {"messages": [{"role": "user", "content": f"Distribute this work: {task}"}]},
                config=config
            )
            logger.info("Coordinator planning complete")
            
            # 2. Spawn workers (simulated)
            batch_size = len(items) // self.num_workers
            worker_results = []
            
            for i in range(self.num_workers):
                start = i * batch_size
                end = start + batch_size if i < self.num_workers - 1 else len(items)
                batch = items[start:end]
                
                # Worker processes batch
                logger.info(f"Worker {i+1} processing {len(batch)} items")
                worker_result = f"Worker_{i+1}_results: Processed {batch}"
                worker_results.append(worker_result)
            
            # 3. Aggregator combines results
            config = {"configurable": {"thread_id": f"{session_id}_aggregator"}}
            agg_result = await aggregator.ainvoke(
                {"messages": [{"role": "user", "content": f"Aggregate these results: {worker_results}"}]},
                config=config
            )
            logger.info("Aggregation complete")
            
            return {
                "coordinator_plan": plan_result,
                "worker_results": worker_results,
                "aggregated": agg_result,
                "status": "success"
            }
            
        except Exception as e:
            logger.error(f"Multi-agent processing failed: {e}")
            return {"error": str(e), "status": "failed"}

async def run_team(task: str, num_workers: int = 5, session_id: str = "default"):
    """Run multi-agent team."""
    team = MultiAgentTeam(num_workers=num_workers)
    
    # Example items to process
    items = [f"item_{i}" for i in range(100)]
    
    result = await team.run(task, items, session_id)
    return result

if __name__ == "__main__":
    task = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Monitor 100 stocks for patterns"
    num_workers = int(os.getenv("NUM_WORKERS", "5"))
    
    result = asyncio.run(run_team(task, num_workers=num_workers))
    print(json.dumps(result, indent=2, default=str))
