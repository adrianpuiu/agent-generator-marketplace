---
description: Initialize a long-running multi-session project with feature tracking, progress logs, and session management
argument-hint: "[project_name] [description]"
---

# Initialize Long-Running Project

Set up a production-ready environment for complex projects spanning multiple context windows and sessions.

Based on Anthropic's long-running agent research, this initializer creates a structured environment that allows agents to make consistent, verifiable progress across days or weeks.

## Perfect For

- Multi-week software projects
- Large data pipelines (100k+ records)
- Complex analysis systems
- Full-stack applications
- Research automation (weeks/months)
- Financial modeling systems
- Infrastructure automation

## Usage

```bash
/initialize-long-running "project name" "detailed description"
```

With options:

```bash
/initialize-long-running "Trading Pipeline" \
  "Build complete order flow analysis system" \
  --features auto \
  --sessions-expected 20 \
  --integrate github,slack

/initialize-long-running "Data Analysis Platform" \
  "Analyze 1M customer records" \
  --feature-count 150 \
  --test-framework pytest \
  --integrate github,monitoring
```

## What Gets Created

### 1. Feature List (`features.json`)
Comprehensive JSON file with all planned features:

```json
[
  {
    "id": "001",
    "category": "core",
    "priority": "critical",
    "description": "Data loader handles CSV files",
    "steps": [
      "Read CSV from path",
      "Parse headers",
      "Validate data types",
      "Load into memory",
      "Verify row count matches"
    ],
    "passes": false,
    "verified_in_session": null,
    "blockers": [],
    "notes": ""
  },
  {
    "id": "002",
    "category": "core",
    "priority": "critical",
    "description": "Data validation catches missing values",
    "steps": [
      "Run validation on loaded data",
      "Identify columns with nulls",
      "Report count of missing values",
      "Suggest handling strategies"
    ],
    "passes": false,
    "verified_in_session": null,
    "blockers": ["001"],
    "notes": ""
  }
]
```

**All features initially `passes: false`** - Prevents premature victory claims

**Strongly-worded instruction:** "It is unacceptable to remove, add, or edit features. Only change the `passes` field."

---

### 2. Progress Log (`claude-progress.txt`)
Session-by-session record of what happened:

```
=== PROJECT: Trading Pipeline Analysis ===
Initialized: 2024-12-09 14:30 UTC
Total Sessions Expected: 20
Goal: Build complete order-flow analysis system

SESSION 1 [2024-12-09, Initializer Agent]
- Set up project structure
- Created 150 feature specifications
- Wrote init.sh for data loading
- Set up git repository
- Verified baseline environment works
- Status: READY FOR SESSION 2

SESSION 2 [2024-12-10 09:00, Coder Agent]
- Worked on features 001-005 (core data loading)
- Feature 001: PASS (CSV loading works)
- Feature 002: PASS (validation catches nulls)
- Feature 003: PASS (type coercion correct)
- Feature 004: FAIL (error handling incomplete)
- Feature 005: NOT ATTEMPTED (blocked by 004)
- Time spent: 35 minutes
- Commits: 3 (see git log)
- Next: Fix feature 004, then continue with 005
- Status: CLEAN STATE (baseline still works)

SESSION 3 [2024-12-10 14:30, Coder Agent]
- Started with 4 passing
- Fixed feature 004 (error handling)
- Feature 004: PASS
- Feature 005: PASS
- Feature 006: PASS
- Feature 007: PARTIAL (needs more testing)
- Time spent: 38 minutes
- Commits: 3
- Next: Complete feature 007, test with real data
- Status: CLEAN STATE
```

---

### 3. Setup Script (`init.sh`)
Executable script to start the development environment:

```bash
#!/bin/bash
set -e

echo "Initializing project environment..."

# Create virtual environment if needed
if [ ! -d "venv" ]; then
  python -m venv venv
fi

source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start services (if applicable)
if [ -f "docker-compose.yml" ]; then
  docker-compose up -d
fi

# Run baseline test
echo "Running baseline verification..."
python -m pytest tests/baseline_test.py -v

if [ $? -eq 0 ]; then
  echo "✓ Environment ready"
  exit 0
else
  echo "✗ Environment setup failed"
  exit 1
fi
```

---

### 4. Git Repository
Initial repository with clear structure:

```
Initial commit message:
"[init] Set up project structure with features and tracking

- Create features.json with 150 feature specifications
- Add claude-progress.txt for session tracking
- Add init.sh for environment setup
- Add requirements.txt and baseline tests
- All features initially marked as incomplete
- Ready for Session 1 work"
```

---

### 5. Testing Baseline
Basic tests to verify environment works:

```python
# tests/baseline_test.py
def test_environment_setup():
    """Verify basic environment is functional"""
    assert os.path.exists("requirements.txt")
    assert os.path.exists("features.json")
    assert os.path.exists("claude-progress.txt")

def test_data_loading():
    """Verify data loader works with sample data"""
    data = load_sample_data()
    assert len(data) > 0
    assert has_required_columns(data)

def test_core_pipeline():
    """End-to-end test of core functionality"""
    result = run_pipeline(sample_data)
    assert result is not None
    assert validate_output_format(result)
```

---

## Real-World Examples

### Example 1: Trading System Initialization

```bash
/initialize-long-running "order_flow_analyzer" \
  "Build complete order-flow analysis with pattern detection, ML models, and backtesting" \
  --features auto \
  --sessions-expected 25 \
  --integrate github,slack,database \
  --test-framework pytest

# Created files:
# - features.json (180 features)
# - claude-progress.txt (ready for Session 1)
# - init.sh (loads data, starts services)
# - requirements.txt (dependencies)
# - tests/baseline_test.py (baseline verification)
# - .git/ (initialized repo)

# First commit:
# "Set up order-flow analyzer with 180 features"
# 
# Next step: Run /work-on-feature for Session 1
```

---

### Example 2: Data Pipeline Initialization

```bash
/initialize-long-running "data_pipeline" \
  "Process 1M customer records, perform analysis, generate reports" \
  --feature-count 120 \
  --test-framework pytest \
  --integrate github,monitoring \
  --scaffold full

# Created:
# - features.json (120 features)
# - claude-progress.txt (session tracking)
# - init.sh (data loading, service startup)
# - Dockerfile (reproducible environment)
# - docker-compose.yml (services)
# - requirements.txt
# - tests/ (baseline tests)
# - configs/ (configuration templates)
```

---

### Example 3: ML System Initialization

```bash
/initialize-long-running "ml_system" \
  "Train models, optimize hyperparameters, deploy to production" \
  --features auto \
  --scaffold ml \
  --integrate github,slack,monitoring \
  --sessions-expected 30

# Created:
# - features.json (150+ ML-specific features)
# - claude-progress.txt
# - init.sh (data loading, model setup)
# - ml_config.yaml (model configurations)
# - Makefile (common commands)
# - requirements.txt (ML libraries)
# - tests/ml_baseline.py
# - notebooks/exploration.ipynb
```

---

## Workflow After Initialization

### Session 1 (Initializer - Already Done)
✅ Environment set up
✅ Features specified
✅ Baseline working
✅ Ready to begin

### Session 2+ (Coding Agent)
```bash
/work-on-feature "project_name" \
  --session 2 \
  --feature-strategy "priority-first" \
  --test-before-complete yes
```

Agent starts by:
1. Reading progress file (understand history)
2. Reading git logs (see recent work)
3. Listing completed features (know what works)
4. Selecting next incomplete feature
5. Running baseline test (catch broken state)
6. Working on ONE feature at a time
7. Testing thoroughly
8. Updating progress file
9. Creating git commit
10. Ensuring clean state

---

## Options

- `--features auto` - Generate features automatically (default)
- `--feature-count N` - Suggest number of features
- `--sessions-expected N` - Hint about project length
- `--test-framework pytest|unittest|custom`
- `--scaffold full|minimal|custom`
- `--integrate github|slack|database|monitoring`
- `--setup-type python|node|rust|custom`

---

## Key Principles

### 1. Feature Completeness
- Features are specified upfront
- Prevents "mission accomplished" early
- Detailed step-by-step descriptions
- Clear pass/fail criteria

### 2. Session Transparency
- Every session logged
- What worked, what didn't
- Time spent per session
- Next session guidance

### 3. Environment Consistency
- init.sh restores environment
- Baseline tests catch problems
- Git history shows progress
- Clean state = mergeable code

### 4. Incremental Work
- One feature per session (or less)
- Test before marking complete
- Commit after each feature
- Leave environment in working state

---

## After Initialization

### Inspect What Was Created
```bash
cat features.json          # See all 150+ planned features
cat claude-progress.txt    # See session log template
cat init.sh               # See environment setup
git log                   # See initial commit
python -m pytest tests/   # Run baseline tests
```

### Start First Coding Session
```bash
/work-on-feature "project_name" \
  --session 1 \
  --feature-count 5 \
  --verify-baseline yes
```

Agent will:
1. Run init.sh to start environment
2. Run baseline tests
3. Select top 5 priority features
4. Work on them incrementally
5. Leave clean state

---

## Customization

Users can customize:
- Feature list format
- Testing approach
- Git commit style
- Session log structure
- Integration services

```bash
/initialize-long-running "project" "description" \
  --feature-template custom.json \
  --test-template my_tests.py \
  --progress-format extended \
  --integrate github,slack,custom-webhook
```

---

## Success Indicators

✅ **Project Initialization:**
- features.json created with 100+ items
- claude-progress.txt ready
- init.sh executable and working
- Git repo initialized
- Baseline tests pass

✅ **Session 1 Completion:**
- 5-10 features working
- Progress file filled in
- Git commits clear
- Baseline still passes
- Clean state achieved

✅ **Multi-Session Success:**
- Consistent progress per session
- No regression (baseline always passes)
- Features marked complete accurately
- Clear handoff between sessions
- Can pick up from progress file

---

## Common Issues & Solutions

**"Features are too granular"**
→ Use `--feature-count` to adjust
→ Combine related features

**"Too many features to implement"**
→ Mark lower-priority as "future"
→ Focus on critical path
→ Phase implementation

**"Baseline tests failing"**
→ Check init.sh script
→ Review dependencies
→ Verify data access

---

## Summary

**`/initialize-long-running` enables:**
- ✅ Multi-session project tracking
- ✅ Structured feature specification
- ✅ Session-to-session continuity
- ✅ Clean state handoffs
- ✅ Progress visibility
- ✅ Multi-week/month projects

**Perfect for:**
- ✅ Complex software projects
- ✅ Data pipelines
- ✅ Research automation
- ✅ Infrastructure as code
- ✅ ML systems
- ✅ Anything multi-session

---

## Next Step

After initialization, run:
```bash
/work-on-feature "project_name" --session 1
```

to begin the first coding session with proper state management.

---

**Based on Anthropic's long-running agent research.**
