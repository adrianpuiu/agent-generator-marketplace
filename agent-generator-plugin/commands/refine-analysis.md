---
description: Refine and improve previous analysis or research results with additional iterations and deeper insights
argument-hint: "[analysis file or previous output]"
---

# Refine Analysis

Generate a refinement DeepAgent that takes previous analysis, research, or problem-solving output and iteratively improves it with more iterations and deeper investigation.

## Perfect For

- Improving previous research or analysis
- Adding more evidence to conclusions
- Exploring alternative perspectives
- Deepening investigation on key findings
- Validating previous recommendations
- Preparing higher-quality reports

## Usage

```
/refine-analysis "previous_analysis.md"
```

With options:

```
/refine-analysis "file.md" --iterations 5
/refine-analysis "file.md" --focus "competitive advantages"
/refine-analysis "file.md" --depth thorough
/refine-analysis "file.md" --memory redis
```

## What You Get

Generated refinement agent includes:

✅ **Iterative Improvement**
- Reads previous analysis
- Identifies gaps and weaknesses
- Generates deeper insights
- Validates findings with new evidence

✅ **Enhancement Framework**
- Adds more sources/data
- Explores alternative perspectives
- Tests assumptions
- Strengthens conclusions

✅ **Result Comparison**
- Shows before/after
- Highlights new findings
- Documents improvements
- Tracks confidence levels

✅ **Memory Persistence**
- Redis for session continuity
- Stores refinement iterations
- Tracks version history

## Workflow

1. **Load Previous Output** - Parse existing analysis
2. **Identify Gaps** - What's missing or weak?
3. **Plan Refinement** - Strategy for deeper investigation
4. **Gather More Data** - Additional sources and evidence
5. **Deepen Analysis** - Explore key areas more thoroughly
6. **Validate Findings** - Test assumptions
7. **Generate Refined Report** - Improved conclusions with evidence

## Real Examples

### Example 1: Enhance Market Research
```
/refine-analysis "quantum_companies_research.md" --iterations 5

Previous analysis was good, but now:
1. Adds funding trajectory analysis
2. Explores team expertise deeper
3. Validates technology claims
4. Adds competitive threat analysis
5. Strengthens investment thesis

Output: quantum_companies_refined.md (more comprehensive)
```

### Example 2: Improve Problem-Solving
```
/refine-analysis "api_optimization_solutions.md" --focus "implementation feasibility"

Previous solutions identified, now:
1. Analyzes implementation complexity
2. Tests feasibility assumptions
3. Identifies potential risks
4. Explores mitigation strategies
5. Ranks by true feasibility

Output: api_optimization_refined.md (more practical)
```

### Example 3: Deepen Data Analysis
```
/refine-analysis "stock_patterns.md" --depth thorough

Initial patterns found, now:
1. Tests statistical significance
2. Explores causation vs correlation
3. Identifies confounding factors
4. Validates across time periods
5. Strengthens pattern confidence

Output: stock_patterns_refined.md (more rigorous)
```

## Options

- `--iterations 5` - Number of refinement iterations (default: 3)
- `--focus "area"` - Specific area to deepen (default: all)
- `--depth thorough` - Refinement depth (default: balanced)
- `--memory redis` - Enable Redis for long refinement sessions

## After Generation

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run refinement
python generated_agent.py previous_analysis.md

# 3. Output
- refined_analysis.md (improved report)
- refinement_summary.md (what changed)
- gap_analysis.json (identified gaps)
- new_findings.md (additional discoveries)
- before_after_comparison.txt (changes documented)
```

## Key Features

- **Iterative Improvement** - Multiple refinement cycles
- **Gap Identification** - Finds weak areas automatically
- **Evidence Gathering** - Stronger conclusions with more data
- **Assumption Testing** - Validates previous claims
- **Before/After** - Clear documentation of improvements
- **Confidence Tracking** - Shows where confidence increased

## Customization

- Adjust refinement focus areas
- Add domain-specific validation tools
- Customize confidence metrics
- Implement custom comparison logic
- Add quality scoring
- Deploy as continuous improvement service

## Use Cases

- **Research** - Improve market or competitive research
- **Problem-Solving** - Strengthen solution recommendations
- **Analysis** - Deepen statistical analysis rigor
- **Due Diligence** - Validate investment findings
- **Strategy** - Improve strategic recommendations
- **Quality** - Enhance report quality before publication

## When to Use

Use when you have:
- Previous analysis that's good but could be better
- Time to invest in deeper investigation
- Specific areas you want to strengthen
- Audience that expects high-quality work
- Complex topics needing multiple perspectives
- Need to validate assumptions

## Result Confidence

- **Initial Analysis:** 70% confidence
- **After Refinement:** 85-95% confidence
- **With 5+ Iterations:** 90%+ confidence

## Iteration Levels

- **Level 1:** Basic refinement (adds 1-2 new perspectives)
- **Level 3:** Medium refinement (explores 3-4 areas deeply)
- **Level 5:** Deep refinement (thorough validation, strong conclusions)
