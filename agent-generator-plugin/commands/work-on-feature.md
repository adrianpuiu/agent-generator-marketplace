---
description: Work on a single feature in a long-running project across multiple sessions with proper state management
argument-hint: "[project_id] [session_number]"
---

# Work On Feature

Execute a single session of a long-running project with proper state management, testing, and handoff protocol.

Each session:
- Reads what's been done before
- Works on ONE feature (or completes partial ones)
- Tests thoroughly
- Leaves clean state
- Updates tracking files
- Creates git commit

## Perfect For

- Continuation of `/initialize-long-running` projects
- Multi-session complex work
- Features that take hours/days
- Projects spanning weeks
- Team handoffs
- Ensuring consistent progress

## Usage

```bash
/work-on-feature "project_id" --session 1
```

With options:

```bash
/work-on-feature "trading_pipeline" --session 2 \
  --features-to-work-on 3 \
  --verify-baseline yes \
  --test-mode end-to-end \
  --integrate github,slack

/work-on-feature "ml_system" --session 15 \
  --priority critical \
  --test-framework pytest \
  --memory redis
```

## Session Protocol

Every session follows this protocol:

### Phase 1: Get Bearings (5-10 minutes)

```
[Agent starts new context window]

1. pwd                           # Verify location
2. cat claude-progress.txt       # Read session history
3. git log --oneline -20         # See recent work
4. cat features.json | grep false | head -10  # See what's left
5. bash init.sh                  # Start environment
6. pytest tests/baseline_test.py # Verify nothing broke
```

**Goal:** Understand state, catch broken baselines, know what to work on

---

### Phase 2: Select Work (2-5 minutes)

Agent reads features.json:

```json
{
  "id": "004",
  "priority": "critical",
  "category": "core",
  "description": "Error handling for malformed data",
  "passes": false,
  "blockers": ["001", "002", "003"],  // All completed
  "notes": "Session 1 attempted but incomplete"
}
```

**Decision Logic:**
1. Find features with `passes: false`
2. Check all blockers are complete
3. Pick highest priority
4. Proceed with implementation

---

### Phase 3: Work Incrementally (20-40 minutes)

**One feature at a time:**

```
[Implement Feature 004]

Step 1: Understand requirement
  - Read feature description
  - Review step-by-step guides
  - Check any notes from previous sessions

Step 2: Code implementation
  - Write minimal code
  - Test locally
  - Commit intermediate progress

Step 3: Manual testing (human-level)
  - Don't just check code
  - Actually run the feature
  - Use test tools (browser, API, data)
  - Verify ALL steps work

Step 4: Update tracking
  - Mark feature as: { "passes": true }
  - Add session number: "verified_in_session": 2
  - Add notes if helpful
```

**Critical:** Features marked complete ONLY after thorough testing

---

### Phase 4: Verify & Commit (5-10 minutes)

```
1. Run baseline tests again
   pytest tests/baseline_test.py
   
   → Must pass, else debug before committing

2. Verify feature still works
   (Re-test the feature manually)

3. Update progress file
   [Added to claude-progress.txt:]
   
   SESSION 2 FEATURES COMPLETED:
   - Feature 004: PASS (error handling works)
   - Feature 005: PASS (validation comprehensive)
   
   Status: CLEAN STATE (baseline still passes)

4. Create git commit
   git commit -m "Complete features 004-005: Error handling and validation
   
   - Implement malformed data handling
   - Add comprehensive validation
   - Both features tested end-to-end
   - All baseline tests passing"
```

---

### Phase 5: Handoff (5 minutes)

Leave clear notes for next session:

```
[At end of session, update claude-progress.txt:]

SESSION 2 COMPLETE [2024-12-10 14:30]
- Started with baseline passing
- Completed features: 004, 005 (both critical)
- Time spent: 42 minutes
- Commits: 2
- Blockers encountered: None
- Bugs fixed: 1 (validation edge case)
- Next session should:
  1. Verify baseline (critical)
  2. Work on features 006-008 (related, should go together)
  3. May need to refactor data loading (see notes)
- Status: CLEAN STATE ✓
```

---

## Real-World Session Example

### Session 2 of Trading Pipeline

```bash
/work-on-feature "trading_pipeline" --session 2 \
  --features-to-work-on 3 \
  --verify-baseline yes
```

**Agent execution:**

```
[1] Get bearings
    $ pwd
    /home/claude/trading_pipeline
    
    $ cat claude-progress.txt
    ...SESSION 1: Initialization complete...
    
    $ git log --oneline -5
    abc1234 [init] Set up project with 180 features
    
    $ bash init.sh
    ✓ Environment ready
    
    $ pytest tests/baseline_test.py
    ======================== test session starts ========================
    PASSED tests/baseline_test.py::test_environment_setup
    PASSED tests/baseline_test.py::test_data_loading
    PASSED tests/baseline_test.py::test_core_pipeline
    ======================== 3 passed in 0.58s ========================

[2] Select work
    Feature 001: Data loader handles CSV files
      - Priority: CRITICAL
      - Status: false (not done)
      - Blockers: none
      - Notes: "Core functionality, must work"
    
    → Select Feature 001

[3] Implement Feature 001
    # Reading CSV file loader code...
    # Implementing csv.reader with validation...
    # Testing with sample_data.csv...
    
    import csv
    import pandas as pd
    
    def load_csv(filepath):
        """Load CSV with validation"""
        df = pd.read_csv(filepath)
        assert df.shape[0] > 0, "Empty CSV"
        assert df.columns.tolist() == EXPECTED_COLS
        return df
    
    # Testing...
    $ python -m pytest tests/test_loader.py -v
    PASSED test_load_valid_csv
    PASSED test_load_handles_nulls
    PASSED test_load_validates_columns

[4] Verify & commit
    $ pytest tests/baseline_test.py
    ======================== 3 passed in 0.58s ========================
    
    $ git add -A
    $ git commit -m "Implement Feature 001: CSV data loader
    
    - Load CSV files with validation
    - Check required columns
    - Handle null values appropriately
    - Tested with sample data
    
    All baseline tests passing."

[5] Continue to Feature 002
    Feature 002: Data validation catches missing values
      - Blockers: [001]  ✓ Complete
      - Status: false (not done)
    
    # Implement validation...
    # Test with data containing nulls...
    
    [Same protocol: implement → test → commit]

[6] Progress update
    Adds to claude-progress.txt:
    
    SESSION 2 [2024-12-10 09:00, Coder Agent]
    - Started with baseline passing
    - Feature 001: PASS (CSV loader working)
    - Feature 002: PASS (validation catches nulls)
    - Time spent: 37 minutes
    - Commits: 2
    - Status: CLEAN STATE ✓
    
    Next session should work on Features 003+
```

---

## Testing Strategy

### Not Sufficient:
❌ Just writing code
❌ Unit tests passing
❌ Running curl commands

### Required:
✅ End-to-end testing
✅ Human-level verification
✅ Actually using the feature
✅ Testing with real data
✅ Verifying all steps work

### Tools for Testing

```bash
# For APIs
curl -X POST http://localhost:8000/analyze -d @sample.json

# For web apps
/use-tool puppeteer  # Browser automation

# For data pipelines
python -c "result = process_data(sample); assert result.valid"

# For ML systems
python -c "model = load_model(); pred = model.predict(X); assert 0 < pred < 1"
```

---

## Failure Modes & Prevention

### Failure Mode 1: Too Much Work
**Problem:** Agent tries to do 10 features in one session, context runs out

**Prevention:** Strongly enforce "one feature at a time"
- Clear instruction: "Work on only ONE feature per session"
- Check feature.json after each to ensure progress
- Force git commit between features

---

### Failure Mode 2: Incomplete Testing
**Problem:** Agent marks feature complete without actually testing it

**Prevention:** Explicit test protocol
- Instruction: "You must test the feature like a human user would"
- Provide testing tools
- Ask for verification steps
- Review test results before marking complete

---

### Failure Mode 3: Broken Baseline
**Problem:** Agent makes changes that break previous features

**Prevention:** Baseline test verification
- Run `pytest tests/baseline_test.py` before every commit
- Fix any failures before proceeding
- If can't fix, revert and document in progress file

---

### Failure Mode 4: Lost Context
**Problem:** Next session doesn't know what was done

**Prevention:** Structured documentation
- claude-progress.txt with every session detail
- Git commits with clear messages
- Feature status tracking in JSON
- Explicit handoff notes

---

## Options

- `--session N` - Session number (required)
- `--features-to-work-on N` - Max features per session (default: 1-3)
- `--verify-baseline yes|no` - Check nothing broke (default: yes)
- `--test-mode unit|integration|end-to-end` (default: end-to-end)
- `--test-framework pytest|unittest|custom`
- `--integrate github|slack|database|monitoring`
- `--memory memory|redis|postgres`
- `--priority critical|high|normal|low` - Filter by priority

---

## Common Patterns

### Pattern 1: Core Features First
```bash
/work-on-feature "project" --session 2 \
  --priority critical \
  --features-to-work-on 3
```
Work on critical features first

---

### Pattern 2: Bug Fixes
```bash
/work-on-feature "project" --session 5 \
  --feature-category "bug-fix" \
  --verify-baseline yes
```
Focus on fixing issues from previous sessions

---

### Pattern 3: Feature Group
```bash
/work-on-feature "project" --session 10 \
  --feature-group "authentication" \
  --features-to-work-on 5
```
Work through related features together

---

## Progress Tracking

### What Gets Updated

**features.json:**
```json
{
  "id": "004",
  "passes": true,                    // ← CHANGED
  "verified_in_session": 2,          // ← CHANGED
  "notes": "Tested with bad data"    // ← CHANGED
}
```

**claude-progress.txt:**
```
SESSION 2 [2024-12-10 09:00]
- Feature 004: PASS (verified in session 2)
- Time spent: 37 minutes
- Commits: 2
- Status: CLEAN STATE
```

**Git:**
```
commit abc1234
Author: Coder Agent
Date:   2024-12-10 09:00:00

    Complete Feature 004: Error handling
    
    - Handle malformed input gracefully
    - Return helpful error messages
    - All baseline tests passing
```

---

## Between Sessions

When starting a new session, agent finds:

```
1. features.json with updated status
   → Knows which features are done
   → Knows which are in progress
   
2. claude-progress.txt with history
   → Knows what was tried
   → Knows what worked/didn't work
   → Knows what to focus on
   
3. Git history showing progress
   → Can revert if needed
   → Can see what changed
   → Can understand decisions
   
4. init.sh that works
   → Can restart environment
   → Can run tests
   → Can verify baseline
```

---

## Success = Clean Handoff

Session is successful when:

✅ **Features completed**
- One or more features marked `passes: true`
- Verified with thorough testing
- All steps work end-to-end

✅ **Clean state**
- Baseline tests still pass
- No broken features
- Code is committable

✅ **Clear documentation**
- Progress file updated
- Git commits meaningful
- Features.json accurate

✅ **Ready for next session**
- Environment still works
- Next session can pick up immediately
- No cleanup needed

---

## After Session Completes

Next session runs:
```bash
/work-on-feature "project" --session 3 \
  --verify-baseline yes
```

And immediately knows:
- What's done (features.json)
- What happened (claude-progress.txt)
- What should be next (priority features)
- If anything broke (baseline test)

---

## Summary

**`/work-on-feature` enforces:**
- ✅ Single feature per session
- ✅ Thorough testing
- ✅ Clean state verification
- ✅ Proper documentation
- ✅ Clear git history
- ✅ Easy handoffs

**Results in:**
- ✅ Consistent progress
- ✅ No regression
- ✅ Accurate tracking
- ✅ Reliable handoffs
- ✅ Multi-week/month projects

---

**Based on Anthropic's long-running agent research.**
