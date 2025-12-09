#!/usr/bin/env python3
"""
Analysis Agent Template - For data exploration with patterns and insights

Generated from /analysis-agent command
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

# === Analysis Planning Tools ===

class AnalysisPlanInput(BaseModel):
    data_type: str = Field(description="Type of data (e.g., stocks, customers, time-series)")
    analysis_goal: str = Field(description="What to find in the data")

@tool(args_schema=AnalysisPlanInput)
def plan_data_analysis(data_type: str, analysis_goal: str) -> str:
    """Create a data analysis plan."""
    logger.info(f"Planning analysis for {data_type}")
    plan = f"""
Data Analysis Plan for {data_type}:
Goal: {analysis_goal}

1. DATA EXPLORATION
   - Load and inspect data
   - Understand structure
   - Check for missing values
   - Statistical summary

2. PATTERN DETECTION
   - Identify correlations
   - Find anomalies
   - Detect trends
   - Segment data

3. HYPOTHESIS TESTING
   - Formulate hypotheses
   - Test with statistics
   - Validate findings
   - Measure confidence

4. VISUALIZATION
   - Create charts
   - Show trends
   - Highlight anomalies
   - Document insights

5. REFINEMENT
   - Drill into patterns
   - Test alternative explanations
   - Validate conclusions
"""
    return plan

class LoadDataInput(BaseModel):
    source: str = Field(description="Data source (CSV, JSON, database)")
    query: str = Field(description="Data to load")

@tool(args_schema=LoadDataInput)
def load_data(source: str, query: str) -> str:
    """Load and explore data."""
    logger.info(f"Loading data from {source}")
    return f"Loaded data from {source}\nShape: [1000 rows x 10 columns]\n[Summary statistics would be displayed]"

class AnalyzePatternInput(BaseModel):
    pattern_type: str = Field(description="Pattern to analyze: correlation, trend, anomaly, cluster")
    data_columns: List[str] = Field(description="Columns to analyze")

@tool(args_schema=AnalyzePatternInput)
def analyze_patterns(pattern_type: str, data_columns: List[str]) -> str:
    """Detect and analyze patterns in data."""
    logger.info(f"Analyzing {pattern_type} patterns")
    return f"Pattern Analysis ({pattern_type}):\nColumns: {data_columns}\n[Detailed pattern analysis would be displayed]"

@tool
def generate_insights() -> str:
    """Generate key insights from analysis."""
    return "Key Insights:\n[Top 5 findings from data exploration]"

@tool
def create_visualization() -> str:
    """Create charts and visualizations."""
    return "Visualizations Created:\n[Charts saved to visualizations/ folder]"

# === Agent Setup ===

all_tools = [
    plan_data_analysis,
    load_data,
    analyze_patterns,
    generate_insights,
    create_visualization,
]

agent = create_deep_agent(
    model="claude-sonnet-4-20250514",
    tools=all_tools,
    system_prompt="""You are a Data Analysis DeepAgent specializing in deep data exploration.

Your approach:
1. Plan data analysis strategy
2. Load and explore data
3. Identify patterns (correlations, trends, anomalies)
4. Test hypotheses
5. Generate insights
6. Create visualizations
7. Refine findings iteratively

Always:
- Plan before analyzing
- Use statistical rigor
- Validate patterns with tests
- Create visualizations
- Document assumptions
- Iterate on findings
""",
    max_iterations=15,
)

async def run_analysis(analysis_query: str, session_id: str = "default"):
    """Run the analysis agent."""
    logger.info(f"Starting analysis: {analysis_query}")
    
    try:
        config = {"configurable": {"thread_id": session_id}}
        
        result = await agent.ainvoke(
            {"messages": [{"role": "user", "content": analysis_query}]},
            config=config
        )
        
        logger.info("Analysis completed successfully")
        return result
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Analyze stock data for patterns and trends."
    
    result = asyncio.run(run_analysis(query))
    print(json.dumps(result, indent=2, default=str))
