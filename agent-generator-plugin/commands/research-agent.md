---
description: Create a research agent that plans and conducts deep investigations with web search and analysis
argument-hint: "[topic or research goal]"
---

# Research Agent

Generate a specialized DeepAgent for conducting deep research with planning, web search, and iterative analysis.

## Perfect For

- Market research and competitive analysis
- Technology trend investigation
- Investment research and due diligence
- Scientific literature analysis
- Industry analysis and forecasting
- Company/product research

## Usage

```
/research-agent "Analyze emerging quantum computing companies and their funding landscape"
```

With options:

```
/research-agent "research topic" --memory redis
/research-agent "research topic" --sources 5
/research-agent "research topic" --depth thorough
```

## What You Get

Generated agent automatically includes:

✅ **Web Search Tools**
- Tavily Search - Real-time web search
- Serper - Search engine optimization
- Company research capabilities

✅ **Planning Tools**
- Research strategy planning
- Task decomposition for investigations
- Source evaluation framework
- Iterative refinement

✅ **Analysis Framework**
- Data extraction and synthesis
- Trend analysis
- Competitive positioning analysis
- Investment thesis generation

✅ **Memory Persistence**
- Redis (long research sessions)
- Stores intermediate findings
- Tracks research iterations

## Workflow

1. **Plan Research Strategy** - Agent creates investigation plan
2. **Search & Gather** - Web search for relevant information
3. **Analyze Findings** - Synthesize and evaluate data
4. **Decompose Further** - Break into deeper sub-questions
5. **Refine Thesis** - Iteratively improve conclusions
6. **Generate Report** - Structured research output

## Real Examples

### Example 1: Market Research
```
/research-agent "What are the top 10 AI healthcare companies? Analyze their technology, funding, and competitive advantages."

Generated agent:
1. Plans research approach
2. Searches for companies
3. Gathers funding/tech data
4. Analyzes competitiveness
5. Generates market thesis
6. Refines findings iteratively
```

### Example 2: Technology Trend Analysis
```
/research-agent "Analyze the current state of quantum computing. Who are the leaders? What are the technical breakthroughs? Commercial timeline?"

Generated agent:
1. Plans investigation scope
2. Searches for latest research
3. Identifies key players
4. Analyzes technical progress
5. Evaluates commercialization timelines
6. Generates comprehensive report
```

### Example 3: Investment Research
```
/research-agent "Deep dive into crypto infrastructure platforms. Analyze market size, competition, technology differentiation, and investment potential."

Generated agent:
1. Plans research framework
2. Searches for platforms
3. Gathers competitive data
4. Analyzes technology
5. Evaluates market opportunity
6. Generates investment thesis
```

## Options

- `--memory redis` - Enable Redis for long research sessions
- `--sources 5` - Number of initial sources to research (default: 3)
- `--depth thorough` - Adjust research depth (default: balanced)

## After Generation

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run research
python generated_agent.py "Your research question"

# 3. Output
- research_findings.md - Structured research report
- sources.json - Research sources and citations
- analysis_summary.txt - Key findings summary
```

## Key Features

- **Deep Investigation** - Multi-step research with planning
- **Iterative Refinement** - Improves findings through iterations
- **Source Tracking** - Maintains research sources
- **Structured Output** - Organized research reports
- **Long Sessions** - Redis memory for extended research
- **Adaptive** - Adjusts research based on findings

## Customization

The generated agent is fully customizable:

- Implement web search with real API keys (Tavily, Serper)
- Add domain-specific analysis tools
- Customize research prompts
- Add citation formatting
- Integrate with research databases
- Deploy as research service

## Use Cases

- **Venture Capital** - Due diligence and market analysis
- **Product Management** - Competitive and market research
- **Strategy** - Industry analysis and trends
- **Sales** - Prospect research and market intelligence
- **Academic** - Literature review and synthesis
- **Journalism** - Investigative research
