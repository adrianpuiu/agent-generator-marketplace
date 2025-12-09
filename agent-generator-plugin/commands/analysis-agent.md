---
description: Create a data analysis agent that explores patterns, correlations, and insights with planning and evaluation
argument-hint: "[dataset description or analysis goal]"
---

# Analysis Agent

Generate a specialized DeepAgent for conducting deep data analysis with planning, pattern detection, and iterative refinement.

## Perfect For

- Data exploration and discovery
- Pattern and anomaly detection
- Correlation analysis
- Market/financial data analysis
- Time-series forecasting
- Business intelligence and metrics analysis

## Usage

```
/analysis-agent "Analyze 10 years of stock price data to identify patterns and predict trends"
```

With options:

```
/analysis-agent "analysis goal" --memory redis
/analysis-agent "analysis goal" --depth thorough
/analysis-agent "analysis goal" --visualize yes
```

## What You Get

Generated agent includes:

✅ **Data Tools**
- Data loading and preprocessing
- Statistical analysis framework
- Pattern detection algorithms
- Correlation analysis

✅ **Planning Tools**
- Analysis strategy planning
- Task decomposition for investigations
- Hypothesis evaluation
- Result refinement

✅ **Visualization**
- Chart generation
- Trend visualization
- Correlation heatmaps
- Time-series plots

✅ **Memory & Output**
- Redis for long analysis sessions
- Structured analysis reports
- Data insights summary

## Workflow

1. **Plan Analysis** - Strategy for exploring data
2. **Load & Explore** - Understand data structure
3. **Analyze Patterns** - Find correlations and trends
4. **Test Hypotheses** - Evaluate findings
5. **Decompose Further** - Drill into interesting patterns
6. **Refine Conclusions** - Iterate on insights

## Real Examples

### Example 1: Stock Analysis
```
/analysis-agent "Analyze price-volume correlations for tech stocks. Identify unusual trading patterns and predict volatility spikes."

Generated agent:
1. Plans analysis approach
2. Loads stock data
3. Analyzes price-volume relationships
4. Detects anomalies
5. Forecasts volatility
6. Generates trading signals
```

### Example 2: Customer Data Analysis
```
/analysis-agent "Analyze customer segmentation. Find behavioral patterns, churn predictors, and lifetime value drivers."

Generated agent:
1. Plans segmentation strategy
2. Explores customer data
3. Identifies behavioral clusters
4. Analyzes churn patterns
5. Calculates lifetime value
6. Generates actionable segments
```

### Example 3: Time-Series Forecasting
```
/analysis-agent "Analyze web traffic data. Identify seasonality, trends, and forecast next quarter's traffic."

Generated agent:
1. Plans forecasting approach
2. Decomposes time-series
3. Identifies seasonality
4. Models trends
5. Forecasts with confidence intervals
6. Refines model iteratively
```

## Options

- `--memory redis` - Enable Redis for long analysis
- `--depth thorough` - Deep analysis with more iterations
- `--visualize yes` - Generate charts and visualizations

## After Generation

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run analysis
python generated_agent.py "Your analysis question"

# 3. Output
- analysis_report.md - Detailed findings
- visualizations/ - Charts and graphs
- insights_summary.json - Key metrics
```

## Key Features

- **Deep Exploration** - Multi-step analysis with planning
- **Pattern Detection** - Find correlations and anomalies
- **Statistical Rigor** - Proper statistical testing
- **Visualization** - Charts for insights
- **Iterative Refinement** - Improves with iterations
- **Exportable** - Reports and visualizations

## Customization

- Load custom datasets (CSV, JSON, databases)
- Add domain-specific analysis functions
- Implement custom ML models
- Add statistical tests
- Integrate with BI tools
- Deploy as analytics service

## Use Cases

- **Finance** - Stock and portfolio analysis
- **Product** - User behavior and metrics
- **Marketing** - Campaign and cohort analysis
- **Operations** - Process optimization analysis
- **Science** - Experimental data analysis
- **Business** - Revenue and growth drivers
