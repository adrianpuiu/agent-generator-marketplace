#!/usr/bin/env python3
"""
Problem Solver Agent Template - For root cause analysis and solution generation

Generated from /problem-solver command
"""

import os
import sys
import logging
from typing import Optional, List
import asyncio
import json

from langgraph.prebuilt import create_deep_agent
from langchain_core.tools import tool
from pydantic import BaseModel, Field

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# === Problem-Solving Tools ===

class ProblemAnalysisInput(BaseModel):
    problem: str = Field(description="Problem statement")
    context: str = Field(description="Business context and constraints")

@tool(args_schema=ProblemAnalysisInput)
def analyze_problem(problem: str, context: str) -> str:
    """Analyze and decompose a problem."""
    logger.info(f"Analyzing problem: {problem}")
    analysis = f"""
Problem Analysis:
Statement: {problem}
Context: {context}

Decomposition:
1. Symptoms vs. Root Causes
2. Key Components
3. Constraint
s
4. Stakeholder Impact
5. Data Needed

[Detailed decomposition would be generated]
"""
    return analysis

class RootCauseInput(BaseModel):
    problem_area: str = Field(description="Area to analyze for root causes")
    hypotheses: List[str] = Field(description="Potential causes to investigate")

@tool(args_schema=RootCauseInput)
def investigate_root_causes(problem_area: str, hypotheses: List[str]) -> str:
    """Investigate potential root causes."""
    logger.info(f"Investigating root causes in {problem_area}")
    return f"Root Cause Investigation:\n{problem_area}\nHypotheses: {hypotheses}\n[Evidence and analysis would be displayed]"

class SolutionInput(BaseModel):
    problem: str = Field(description="Problem to solve")
    constraints: List[str] = Field(description="Implementation constraints")
    num_solutions: int = Field(default=3, description="Number of solutions to generate")

@tool(args_schema=SolutionInput)
def generate_solutions(problem: str, constraints: List[str], num_solutions: int = 3) -> str:
    """Generate multiple solutions to a problem."""
    logger.info(f"Generating {num_solutions} solutions")
    solutions = f"""
Generated Solutions for: {problem}
Constraints: {constraints}

Solution 1: [Approach A with rationale]
Solution 2: [Approach B with rationale]
Solution 3: [Approach C with rationale]

[More detailed solutions would be generated]
"""
    return solutions

class EvaluateInput(BaseModel):
    solutions: List[str] = Field(description="Solutions to evaluate")
    criteria: List[str] = Field(description="Evaluation criteria")

@tool(args_schema=EvaluateInput)
def evaluate_solutions(solutions: List[str], criteria: List[str]) -> str:
    """Evaluate and rank solutions."""
    logger.info(f"Evaluating {len(solutions)} solutions")
    return "Solution Evaluation:\n[Scoring matrix and rankings would be displayed]"

@tool
def generate_recommendations() -> str:
    """Generate final recommendations with implementation plan."""
    return "Recommendations:\n[Top-ranked solution with implementation steps]"

# === Agent Setup ===

all_tools = [
    analyze_problem,
    investigate_root_causes,
    generate_solutions,
    evaluate_solutions,
    generate_recommendations,
]

agent = create_deep_agent(
    model="claude-sonnet-4-20250514",
    tools=all_tools,
    system_prompt="""You are a Problem Solver DeepAgent specializing in systematic problem-solving.

Your approach:
1. Analyze and decompose the problem
2. Investigate root causes
3. Generate multiple solution approaches
4. Evaluate solutions against criteria
5. Rank by feasibility and impact
6. Create implementation plan
7. Refine recommendations iteratively

Always:
- Distinguish symptoms from root causes
- Generate multiple solutions
- Evaluate objectively
- Consider constraints
- Provide actionable recommendations
- Document reasoning
""",
    max_iterations=15,
)

async def solve_problem(problem_statement: str, session_id: str = "default"):
    """Run the problem solver agent."""
    logger.info(f"Starting problem analysis: {problem_statement}")
    
    try:
        config = {"configurable": {"thread_id": session_id}}
        
        result = await agent.ainvoke(
            {"messages": [{"role": "user", "content": problem_statement}]},
            config=config
        )
        
        logger.info("Problem solving completed")
        return result
    except Exception as e:
        logger.error(f"Problem solving failed: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "API latency is 500ms. Find root causes and propose solutions."
    
    result = asyncio.run(solve_problem(query))
    print(json.dumps(result, indent=2, default=str))
