# Long-Running Agent Patterns

Comprehensive guide to managing multi-session projects with proper state management, based on Anthropic research.

## The Core Problem

Multi-session projects fail because:

1. **Context amnesia** - Agent starts fresh each session with no memory
2. **Scope creep** - Agent tries to do too much, runs out of context
3. **Premature completion** - Agent declares victory too early
4. **No handoff protocol** - Next session doesn't know what to do
5. **Broken state** - Changes break existing functionality
6. **Incomplete testing** - Features marked done without real verification

## The Solution

**Two-part framework:**

1. **Initializer Agent** (Session 1)
   - Sets up environment
   - Specifies all features
   - Creates tracking files
   - Establishes baseline

2. **Coder Agent** (Sessions 2+)
   - Gets bearings from tracking files
   - Works incrementally (one feature)
   - Tests thoroughly before marking done
   - Leaves clean state
   - Documents handoff

---

## Pattern 1: Feature Specification

### Problem
Agent doesn't know the full scope, so it over-commits or declares victory early.

### Solution
Comprehensive feature list in JSON format (not editable by coding agents):

```json
[
  {
    "id": "001",
    "priority": "critical",
    "category": "core",
    "description": "System loads data from CSV files",
    "steps": [
      "Read CSV file from provided path",
      "Parse headers correctly",
      "Validate that all required columns exist",
      "Load all rows into memory",
      "Verify row count matches file size"
    ],
    "acceptance_criteria": [
      "Function returns DataFrame with correct shape",
      "Column names match expected schema",
      "Data types are appropriate"
    ],
    "passes": false,
    "verified_in_session": null,
    "depends_on": [],
    "blocker_for": ["002", "003"],
    "notes": "",
    "tags": ["data-loading", "required"]
  }
]
```

### Why This Works
- ✅ Agents can't remove features (prevents early victory)
- ✅ Clear acceptance criteria (prevents premature marking)
- ✅ Dependencies tracked (prevents working on wrong feature)
- ✅ JSON format (less likely to be corrupted vs Markdown)

### Best Practices
- Feature descriptions should be 2-3 sentences max
- Steps should be action-oriented ("user sees...", "system returns...")
- Include acceptance criteria (quantifiable)
- Mark all initially as `passes: false`
- Include strong instruction: "It is unacceptable to remove, add, or edit features"

---

## Pattern 2: Session State Management

### Problem
Agent starting new session doesn't know what happened before.

### Solution
Structured progress file with every session documented:

```
=== PROJECT: Trading Analysis System ===
Initialized: 2024-12-09 14:30 UTC
Total Features: 180
Completion Target: 100%

SUMMARY:
- Sessions completed: 8
- Features passing: 42 / 180 (23%)
- Average features per session: 5.25
- Estimated completion: Session 18-20

═══════════════════════════════════════════

SESSION 1 [2024-12-09 14:30, Type: INITIALIZER]
Agent: System Initializer
Duration: Initialization
Status: COMPLETE

Actions:
- Specified 180 features in features.json
- Created init.sh for environment setup
- Set up baseline tests
- Initialized git repository
- Verified environment works

Output:
- features.json (180 features)
- init.sh (executable)
- requirements.txt
- tests/baseline_test.py
- Initial git commit

Result: READY FOR CODING

═══════════════════════════════════════════

SESSION 2 [2024-12-10 09:00, Type: CODER]
Agent: Coder-001
Duration: 45 minutes
Status: COMPLETE

Baseline Status: PASS (verified at start and end)

Features Attempted: 6
- Feature 001: PASS (data loading works perfectly)
- Feature 002: PASS (validation catches nulls)
- Feature 003: PASS (type coercion correct)
- Feature 004: FAIL (error handling incomplete, see notes)
- Feature 005: BLOCKED (depends on 004)
- Feature 006: NOT ATTEMPTED (lower priority)

Commits: 3
- "Implement data loading pipeline"
- "Add validation for null values"
- "Fix type coercion edge cases"

Issues Encountered:
- Feature 004 had edge case with unicode errors
- Needs better error messages
- Suggestion: Refactor error handling next session

Next Session Guidance:
1. Start by verifying baseline (critical!)
2. Feature 004 is highest priority (fix the error handling)
3. Then work on features 005-007
4. May want to refactor data validation (see commits)

Status: CLEAN STATE ✓
All features that passed are fully functional
No technical debt introduced

═══════════════════════════════════════════

SESSION 3 [2024-12-10 14:30, Type: CODER]
Agent: Coder-002
Duration: 38 minutes
Status: COMPLETE

Baseline Status: PASS

Features Attempted: 5
- Feature 004: PASS (fixed error handling)
- Feature 005: PASS (validation of ranges works)
- Feature 006: PARTIAL (needs more testing)
- Feature 007: NOT ATTEMPTED
- Feature 008: NOT ATTEMPTED (should save for next)

Commits: 2
- "Fix feature 004: Better error handling"
- "Implement feature 005: Range validation"

Issues Encountered:
- Feature 006 needs testing with larger datasets
- Error messages could be more helpful

Next Session Guidance:
1. Complete feature 006 (finish testing)
2. Work on features 007-009
3. Consider refactoring validation module (is getting large)

Status: CLEAN STATE ✓
Baseline all passing
Ready for continuation

═══════════════════════════════════════════
```

### Why This Works
- ✅ Next session knows exact state
- ✅ Can see what failed and why
- ✅ Clear guidance for next session
- ✅ Historical record of progress
- ✅ Easy to spot patterns/issues

### Best Practices
- Log every session with consistent format
- Include baseline test results
- Note any issues or blockers
- Provide explicit guidance for next session
- Track time spent (identify long/short sessions)
- Mark final state (clean/dirty)

---

## Pattern 3: Environment Setup Script

### Problem
Each session needs to start environment, but agent doesn't know how.

### Solution
Automated init.sh script:

```bash
#!/bin/bash
set -e

echo "═══════════════════════════════════════════"
echo "  Initializing Project Environment"
echo "═══════════════════════════════════════════"

# Step 1: Virtual environment
echo "[1/5] Setting up Python environment..."
if [ ! -d "venv" ]; then
  python3 -m venv venv
fi
source venv/bin/activate

# Step 2: Dependencies
echo "[2/5] Installing dependencies..."
pip install -q -r requirements.txt

# Step 3: Database/Services
echo "[3/5] Starting services..."
if [ -f "docker-compose.yml" ]; then
  docker-compose up -d > /dev/null 2>&1
  sleep 3  # Wait for services
fi

# Step 4: Baseline data
echo "[4/5] Preparing baseline data..."
if [ ! -f "data/sample_data.csv" ]; then
  python scripts/generate_sample_data.py
fi

# Step 5: Verification
echo "[5/5] Verifying environment..."
python -m pytest tests/baseline_test.py -q

if [ $? -eq 0 ]; then
  echo "═══════════════════════════════════════════"
  echo "  ✓ Environment ready"
  echo "═══════════════════════════════════════════"
  exit 0
else
  echo "═══════════════════════════════════════════"
  echo "  ✗ Environment setup failed"
  echo "═══════════════════════════════════════════"
  exit 1
fi
```

### Why This Works
- ✅ One command to restore environment
- ✅ Idempotent (safe to run multiple times)
- ✅ Verifies everything works before proceeding
- ✅ Agent doesn't need to remember steps

### Best Practices
- Make script idempotent (can run anytime)
- Include verification step
- Clear progress messages
- Handle errors gracefully
- Document non-obvious dependencies

---

## Pattern 4: Baseline Testing

### Problem
Agent doesn't know if previous sessions broke anything.

### Solution
Lightweight baseline test that verifies core functionality:

```python
# tests/baseline_test.py
import pytest
from src.data_loader import load_csv
from src.pipeline import run_pipeline
import tempfile
import pandas as pd

class TestBaseline:
    """Baseline tests that must always pass"""
    
    def test_environment_configured(self):
        """Verify environment is set up correctly"""
        import os
        assert os.path.exists("requirements.txt")
        assert os.path.exists("features.json")
        assert os.path.exists("claude-progress.txt")
    
    def test_data_loader_works(self):
        """Verify core data loading functionality"""
        # Create sample CSV
        df = pd.DataFrame({
            'id': [1, 2, 3],
            'value': [10.5, 20.3, 15.8],
            'category': ['A', 'B', 'A']
        })
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            df.to_csv(f.name, index=False)
            
            # Test loading
            loaded = load_csv(f.name)
            assert loaded.shape == (3, 3)
            assert 'id' in loaded.columns
            assert loaded['value'].dtype == float
    
    def test_pipeline_core_features(self):
        """Verify basic pipeline works"""
        sample_df = pd.DataFrame({
            'id': [1, 2, 3],
            'value': [10, 20, 30]
        })
        
        result = run_pipeline(sample_df)
        assert result is not None
        assert len(result) > 0
    
    def test_no_import_errors(self):
        """Verify main modules import successfully"""
        from src import data_loader
        from src import pipeline
        from src import validation
        assert data_loader is not None
        assert pipeline is not None
        assert validation is not None
```

### Why This Works
- ✅ Quick (runs in seconds)
- ✅ Covers core functionality
- ✅ Fails if something broke
- ✅ Forces environment verification

### Best Practices
- Keep tests minimal (5-10 quick checks)
- Focus on absolutely core functionality
- Should run in < 30 seconds
- Test environment AND code
- Use fixtures for sample data

---

## Pattern 5: Incremental Feature Implementation

### Problem
Agent tries to implement too much, runs out of context, leaves things incomplete.

### Solution
Strict protocol: ONE feature per session (or one feature group)

**The Process:**

```
Session Protocol:
1. Get bearings (5 min)
   - Run init.sh
   - Read progress file
   - Check git log
   - Run baseline tests
   
2. Select work (2 min)
   - Read features.json
   - Find first incomplete feature
   - Check dependencies satisfied
   
3. Implement (20-40 min)
   - Write code
   - Test locally
   - Verify all steps
   - DON'T move to next feature
   
4. Verify & commit (5 min)
   - Run baseline tests
   - Mark feature as complete
   - Create git commit
   - Update progress file
   
5. Done (don't do more!)
   - Leave on good note
   - Let next session continue
```

### Why This Works
- ✅ Forces focus and completeness
- ✅ Prevents context exhaustion
- ✅ Ensures testing happens
- ✅ Easier handoff

### Common Mistakes
❌ Implementing 5 features per session
❌ Skipping testing
❌ Not committing between features
❌ Not updating progress file
❌ Trying to do "just one more"

---

## Pattern 6: Testing Strategy

### Problem
Agent marks feature complete without actually testing it.

### Solution
Explicit testing protocol - human-level verification:

```
Feature: "User can upload CSV and see data preview"

Human-level test (what the agent must do):
1. Actually load a CSV file
2. Verify data preview shows correct columns
3. Test with bad data (empty file, missing columns)
4. Verify error messages appear
5. Test with large file (verify performance)

NOT sufficient:
❌ "Code looks good"
❌ "Unit tests pass"
❌ Just checking syntax

Required:
✅ Actually run the feature
✅ Use it like a user would
✅ Test edge cases
✅ Verify it works end-to-end
```

### Tools for Testing
```bash
# For APIs
curl -X POST http://localhost:8000/api \
  -H "Content-Type: application/json" \
  -d '{"data": "test"}'

# For CLIs
python -m src.cli --input test.csv --output result.json
verify result.json has expected structure

# For data pipelines
df = load_csv('test_data.csv')
result = process(df)
assert result.shape == expected_shape

# For web apps
Use Puppeteer or browser automation
Actually navigate the UI
Verify what displays
```

---

## Pattern 7: Git Commit Strategy

### Problem
Git history doesn't show what happened, making recovery difficult.

### Solution
Meaningful commits with context:

```bash
# GOOD
git commit -m "Implement feature 004: Error handling for malformed data

- Add validation for required fields
- Return helpful error messages
- Handle unicode/encoding errors
- Tested with sample malformed data
- All baseline tests passing

Closes feature 004"

# BAD
git commit -m "Update code"
git commit -m "Fix bugs"
git commit -m "Testing"
```

### Best Practices
- One commit per feature
- Include feature ID in message
- Describe what changed and why
- Mention testing done
- Reference any issues/blockers

---

## Pattern 8: Failure Recovery

### Problem
Agent breaks something, doesn't know how to recover.

### Solution
Use git to recover from bad changes:

```bash
# If something breaks during a session:

1. Identify the problem
   $ pytest tests/baseline_test.py
   FAILED test_core_pipeline

2. See what changed
   $ git diff

3. Options:
   a) Fix the code (if small change)
   b) Revert last commit (if major change)
      $ git revert HEAD
   c) Revert to known good (if stuck)
      $ git reset --hard <good-commit>

4. Update progress file
   "Session 5: Attempted feature 010, broke feature 004,
    reverted to last working commit. Feature 010 still needs work."

5. Move forward carefully
   Work on different feature or fix incrementally
```

### Why This Works
- ✅ Git provides safety net
- ✅ Can always return to working state
- ✅ History shows what went wrong
- ✅ Next session informed of issues

---

## Common Patterns in Real Projects

### Pattern A: Bug Fix Session
Sometimes a session needs to fix bugs from previous sessions:

```
SESSION 12 [Bug Fix]
Baseline Status: FAIL (test_validation_edge_case failing)

Actions:
1. Identified bug: unicode characters in data cause error
2. Root cause: validation function assumes ASCII
3. Fixed: Updated validation to handle Unicode
4. Tested: Verified with Unicode test data
5. Result: All baseline tests passing

Features worked on: 0 new
Bugs fixed: 1
Status: CLEAN STATE ✓
```

### Pattern B: Refactoring Session
Sometimes code needs cleanup:

```
SESSION 15 [Refactoring]
Baseline Status: PASS

Actions:
1. Reviewed progress file suggestions
2. Consolidation: data_loader.py and validation.py
3. Created unified data_processing module
4. Tests: All still pass
5. Result: Cleaner codebase

Commits: 1 (refactoring commit)
Status: CLEAN STATE ✓
Features worked on: 0
Improvement: Code maintainability
```

---

## Metrics to Track

**Per Session:**
- ✅ Number of features completed
- ✅ Time spent
- ✅ Number of commits
- ✅ Baseline test status
- ✅ Issues encountered

**Overall Project:**
- ✅ Features passing / total
- ✅ Estimated sessions remaining
- ✅ Average progress per session
- ✅ Burn-down rate

---

## Summary

**Long-running agent patterns solve:**
- ✅ Context amnesia (progress files)
- ✅ Scope creep (feature lists)
- ✅ Premature completion (testing protocol)
- ✅ Broken state (baseline tests)
- ✅ Lost context (git + documentation)
- ✅ No handoff (structured progress)

**Results:**
- ✅ Consistent progress across sessions
- ✅ Complex projects completed
- ✅ No regression
- ✅ Clear visibility
- ✅ Multi-week/month projects viable

**Key Success Factor:**
Treat agents like human developers:
- Clear scope (feature list)
- Clear context (progress file)
- Clear expectations (one feature)
- Clear testing (verify before done)
- Clear handoff (documentation)

---

**Based on Anthropic's long-running agent research.**
