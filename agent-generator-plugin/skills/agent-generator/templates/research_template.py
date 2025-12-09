#!/usr/bin/env python3
"""
Research Agent Template - For deep investigation with planning and web search

Generated from /research-agent command
"""

import os
import sys
import logging
from typing import Optional
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

# === Research Planning Tools ===

class ResearchPlanInput(BaseModel):
    topic: str = Field(description="The research topic")
    depth: str = Field(description="Research depth: quick, balanced, thorough")

@tool(args_schema=ResearchPlanInput)
def plan_research_strategy(topic: str, depth: str = "balanced") -> str:
    """Create a research strategy for investigating a topic."""
    logger.info(f"Planning research for topic: {topic}")
    strategy = f"""
Research Strategy for: {topic}
Depth Level: {depth}

1. INITIAL SEARCH
   - Identify key players/companies
   - Find recent news and updates
   - Gather funding/market data

2. DEEP DIVE
   - Analyze competitive positioning
   - Examine technology/product
   - Research leadership team

3. SYNTHESIS
   - Identify market opportunities
   - Assess competitive threats
   - Generate key insights
   
4. REFINEMENT
   - Validate findings
   - Identify information gaps
   - Generate conclusions
"""
    return strategy

class SearchInput(BaseModel):
    query: str = Field(description="Search query")
    num_results: int = Field(default=5, description="Number of results")

@tool(args_schema=SearchInput)
def web_search(query: str, num_results: int = 5) -> str:
    """Search the web for information."""
    logger.info(f"Searching for: {query}")
    return f"Found {num_results} results for: {query}\n[Results would include real data from Tavily/Serper]"

class AnalysisInput(BaseModel):
    findings: str = Field(description="Research findings to analyze")
    focus: str = Field(description="Analysis focus area")

@tool(args_schema=AnalysisInput)
def analyze_findings(findings: str, focus: str) -> str:
    """Analyze and synthesize research findings."""
    logger.info(f"Analyzing findings with focus: {focus}")
    return f"Analysis of {focus}:\n{findings[:100]}...\n[Detailed analysis would be generated]"

# === Research-Specific Tools ===

@tool
def generate_research_thesis() -> str:
    """Generate investment or market thesis from research."""
    return "Research Thesis: [Generated based on findings]"

@tool
def evaluate_sources(sources: list = None) -> str:
    """Evaluate credibility and relevance of sources."""
    return "Source Evaluation: [Credibility scores and relevance]"

# === Agent Setup ===

all_tools = [
    plan_research_strategy,
    web_search,
    analyze_findings,
    generate_research_thesis,
    evaluate_sources,
]

agent = create_deep_agent(
    model="claude-sonnet-4-20250514",
    tools=all_tools,
    system_prompt="""You are a Research DeepAgent specializing in deep investigations.

Your approach:
1. Plan a research strategy for the topic
2. Search for reliable sources
3. Gather and analyze findings
4. Decompose complex topics into subtopics
5. Evaluate and synthesize information
6. Iteratively refine your thesis

Always:
- Plan before searching
- Evaluate source credibility
- Track research iterations
- Generate evidence-based conclusions
- Refine findings based on new information
""",
    max_iterations=15,
)

async def run_research(research_query: str, session_id: str = "default"):
    """Run the research agent."""
    logger.info(f"Starting research for: {research_query}")
    
    try:
        config = {"configurable": {"thread_id": session_id}}
        
        result = await agent.ainvoke(
            {"messages": [{"role": "user", "content": research_query}]},
            config=config
        )
        
        logger.info("Research completed successfully")
        return result
    except Exception as e:
        logger.error(f"Research failed: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Research emerging AI healthcare companies and analyze their funding."
    
    result = asyncio.run(run_research(query))
    print(json.dumps(result, indent=2, default=str))
