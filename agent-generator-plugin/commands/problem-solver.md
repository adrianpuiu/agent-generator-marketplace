---
description: Create a problem-solving agent that conducts root cause analysis and generates solutions with planning and evaluation
argument-hint: "[problem statement]"
---

# Problem Solver

Generate a specialized DeepAgent for systematic problem-solving with root cause analysis, solution generation, and evaluation.

## Perfect For

- Root cause analysis (RCA)
- System optimization and debugging
- Business process improvement
- Strategy and planning challenges
- Decision-making support
- Technical and operational problem-solving

## Usage

```
/problem-solver "API latency is 500ms. Identify root causes and propose optimization solutions."
```

With options:

```
/problem-solver "problem" --memory redis
/problem-solver "problem" --depth thorough
/problem-solver "problem" --num-solutions 5
```

## What You Get

Generated agent includes:

✅ **Problem-Solving Tools**
- Root cause analysis framework
- Hypothesis generation
- Impact assessment
- Solution evaluation criteria

✅ **Planning Tools**
- Problem decomposition
- Investigation strategy
- Solution evaluation
- Iterative refinement

✅ **Analysis Framework**
- Causal chain analysis
- Bottleneck identification
- Risk assessment
- Solution ranking

✅ **Structured Output**
- Problem statement
- Root cause findings
- Generated solutions
- Recommendations with rationale

## Workflow

1. **Define Problem** - Clarify scope and impact
2. **Plan Investigation** - Strategy for analysis
3. **Analyze Root Causes** - Deep causal analysis
4. **Decompose Problem** - Break into components
5. **Generate Solutions** - Create multiple approaches
6. **Evaluate Solutions** - Rate against criteria
7. **Refine & Rank** - Iterate on best solutions

## Real Examples

### Example 1: Technical Debugging
```
/problem-solver "Our database queries are slow. Some queries take 30+ seconds. Performance degrades during peak hours."

Generated agent:
1. Plans investigation approach
2. Identifies query bottlenecks
3. Analyzes index usage
4. Examines connection pooling
5. Proposes optimization solutions
6. Ranks solutions by impact
```

### Example 2: Business Process Improvement
```
/problem-solver "Customer onboarding takes 5 days. We need to reduce to 24 hours. What are the bottlenecks?"

Generated agent:
1. Plans process analysis
2. Maps onboarding steps
3. Identifies time sinks
4. Analyzes dependencies
5. Generates improvement solutions
6. Evaluates implementation effort
```

### Example 3: Strategic Problem-Solving
```
/problem-solver "Our market share declined 10% this quarter despite increased marketing spend. What's happening?"

Generated agent:
1. Plans competitive analysis
2. Decomposes contributing factors
3. Analyzes market dynamics
4. Evaluates competitive threats
5. Proposes strategic solutions
6. Ranks by potential impact
```

## Options

- `--memory redis` - Enable Redis for long sessions
- `--depth thorough` - Deep analysis with more iterations
- `--num-solutions 5` - Number of solutions to generate (default: 3)

## After Generation

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run problem-solver
python generated_agent.py "Your problem statement"

# 3. Output
- problem_analysis.md - Problem breakdown
- root_causes.json - Identified causes
- solutions.md - Generated solutions with evaluation
- recommendations.txt - Ranked recommendations
```

## Key Features

- **Systematic Analysis** - Structured problem-solving
- **Multiple Solutions** - Generates diverse approaches
- **Evaluation Framework** - Rates solutions rigorously
- **Root Cause Focus** - Addresses underlying issues
- **Implementation Ready** - Ranked, actionable solutions
- **Iterative Refinement** - Improves through iterations

## Customization

- Customize evaluation criteria
- Add domain-specific analysis tools
- Implement domain constraints
- Add cost/benefit calculators
- Integrate with project management
- Deploy as decision support service

## Use Cases

- **Operations** - Process optimization
- **Engineering** - Technical debugging
- **Product** - Feature and design decisions
- **Strategy** - Business challenges
- **Quality** - Defect root cause analysis
- **Management** - Organizational issues
