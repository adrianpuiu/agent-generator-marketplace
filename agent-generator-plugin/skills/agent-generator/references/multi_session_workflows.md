# Multi-Session Workflows

Real-world examples and templates for projects spanning multiple context windows.

## Workflow 1: Trading Pipeline (25 Sessions, 2 Weeks)

### Project Scope
Build complete order-flow analysis system with pattern detection and backtesting.

### Initialization
```bash
/initialize-long-running "trading_pipeline" \
  "Order-flow analysis with pattern detection, ML models, backtesting" \
  --features auto \
  --sessions-expected 25 \
  --integrate github,slack,monitoring
```

**Creates:**
- features.json (180 features)
- 25 planned sessions × 5-7 features/session = 125-175 expected completions

### Session Breakdown

**Sessions 1-3: Core Data Pipeline** (3 sessions)
- Load market data
- Validate data integrity
- Implement order flow normalization

**Sessions 4-8: Data Analysis** (5 sessions)
- Calculate statistical metrics
- Detect patterns
- Build features for ML

**Sessions 9-15: ML Models** (7 sessions)
- Train models
- Optimize hyperparameters
- Cross-validate
- Generate predictions

**Sessions 16-22: Backtesting** (7 sessions)
- Implement backtesting framework
- Run historical tests
- Calculate Sharpe ratios
- Identify edge cases

**Sessions 23-25: Polish & Optimization** (3 sessions)
- Performance optimization
- Code cleanup
- Documentation

### Timeline
```
Day 1:  Sessions 1-5 (initialization + core pipeline)
Day 2:  Sessions 6-10 (data analysis + early ML)
Day 3:  Sessions 11-15 (ML training)
Day 4:  Sessions 16-20 (backtesting)
Day 5:  Sessions 21-25 (finalization)
```

### Real Session Example

**Session 7: Implement Feature Statistics**
```bash
/work-on-feature "trading_pipeline" --session 7 \
  --features-to-work-on 4 \
  --verify-baseline yes
```

Progress file entry:
```
SESSION 7 [2024-12-10 16:00]
Agent: Coder-003
Duration: 42 minutes
Baseline Status: PASS

Features Completed:
- Feature 045: Calculate OHLC statistics ✓
- Feature 046: Compute volume patterns ✓
- Feature 047: Detect gaps ✓
- Feature 048: Calculate momentum ✓

Commits: 2
- "Implement OHLC statistics and volume analysis"
- "Add gap and momentum calculations"

Baseline Status: PASS ✓
Status: CLEAN STATE
```

---

## Workflow 2: Data Processing System (15 Sessions, 1 Week)

### Project Scope
Process 1M customer records, detect anomalies, generate reports.

### Initialization
```bash
/initialize-long-running "data_processor" \
  "Process 1M records, detect anomalies, generate reports" \
  --features auto \
  --sessions-expected 15 \
  --scaffold full \
  --integrate github,database
```

### Session Breakdown

**Session 1:** Initialization
- Feature specification (120 features)
- Sample data creation
- Environment setup

**Sessions 2-4:** Data Loading (3 sessions)
- Load CSV files
- Handle large datasets
- Validate data quality

**Sessions 5-8:** Anomaly Detection (4 sessions)
- Statistical methods
- ML-based detection
- Ensemble approaches

**Sessions 9-12:** Reporting (4 sessions)
- Generate reports
- Create visualizations
- Export results

**Sessions 13-15:** Optimization (3 sessions)
- Performance tuning
- Parallel processing
- Final testing

### Key Metrics
```
Input: 1,000,000 records
Expected Processing: 30 seconds per session
Output: Anomaly reports, statistics, visualizations
Quality: 99%+ accuracy
```

---

## Workflow 3: Full-Stack Web Application (40 Sessions, 1 Month)

### Project Scope
Build complete web application with frontend, API, database.

### Initialization
```bash
/initialize-long-running "claude_ai_clone" \
  "Build claude.ai clone with chat, history, settings" \
  --features auto \
  --sessions-expected 40 \
  --scaffold full \
  --integrate github,slack,monitoring
```

Creates:
- features.json (200+ features)
- init.sh (starts React dev server + API)
- Baseline tests (verify app loads)

### Session Distribution

**Frontend** (10 sessions)
- UI components
- State management
- Styling

**API** (12 sessions)
- Authentication
- Chat endpoints
- Data persistence

**Database** (8 sessions)
- Schema design
- Migrations
- Optimization

**Integration** (5 sessions)
- Frontend-API integration
- End-to-end testing
- Bug fixes

**Deployment** (5 sessions)
- Production setup
- Performance tuning
- Security hardening

### Typical Session (Frontend)

**Session 8: Implement Chat History**
```bash
/work-on-feature "claude_ai_clone" --session 8 \
  --features-to-work-on 3 \
  --test-mode end-to-end \
  --integrate github,slack
```

```
Features:
- Feature 045: Load chat history from database
- Feature 046: Display history in sidebar
- Feature 047: Navigate between conversations

Session workflow:
1. npm run dev (start servers)
2. npm run test (baseline)
3. Implement features 045-047
4. Test with Puppeteer (actually use app)
5. Git commit
6. npm run test (verify baseline)
7. Update progress file
```

---

## Workflow 4: ML Research Project (20 Sessions, 3 Weeks)

### Project Scope
Develop machine learning model for customer churn prediction.

### Initialization
```bash
/initialize-long-running "churn_prediction" \
  "Build ML model for customer churn prediction" \
  --features auto \
  --scaffold ml \
  --sessions-expected 20 \
  --integrate github,monitoring
```

### Session Distribution

**Data Preparation** (4 sessions)
- Load data
- Handle missing values
- Feature engineering

**Exploratory Analysis** (3 sessions)
- Statistical analysis
- Visualization
- Pattern discovery

**Model Development** (6 sessions)
- Train baseline
- Try different algorithms
- Hyperparameter tuning

**Evaluation** (4 sessions)
- Cross-validation
- Performance metrics
- Error analysis

**Deployment** (3 sessions)
- Model packaging
- API creation
- Performance monitoring

### Session Example (Model Development)

**Session 12: Gradient Boosting Implementation**
```
Features to implement:
- Feature 078: Load preprocessed data
- Feature 079: Train XGBoost model
- Feature 080: Evaluate performance
- Feature 081: Save trained model

Session work:
1. python scripts/setup.py (environment)
2. pytest tests/baseline_test.py (verify)
3. Implement XGBoost training
4. Cross-validation with 5 folds
5. Calculate metrics (AUC, F1, etc.)
6. Save model to disk
7. pytest tests/ (verify everything still works)
8. git commit -m "Implement XGBoost model"
```

---

## Workflow 5: Data Pipeline (12 Sessions, 1 Week)

### Project Scope
ETL pipeline: Extract data, transform, load to data warehouse.

### Initialization
```bash
/initialize-long-running "etl_pipeline" \
  "ETL: Extract from APIs, transform, load to warehouse" \
  --features auto \
  --sessions-expected 12 \
  --integrate github,slack,database
```

### Session Distribution

**Extraction** (3 sessions)
- API connectors
- Data validation
- Error handling

**Transformation** (4 sessions)
- Data cleaning
- Normalization
- Aggregation

**Loading** (3 sessions)
- Database schema
- Bulk loading
- Verification

**Monitoring** (2 sessions)
- Logging
- Alerting
- Performance monitoring

---

## Cross-Workflow Patterns

### Pattern A: Feature Completion Rate
```
Session 1: Initialization
Session 2-5: 7 features/session = 28 total
Session 6-10: 5 features/session = 25 total  (getting harder)
Session 11-15: 3 features/session = 15 total (complex features)
Session 16-20: 2 features/session = 10 total (final polish)

Total: ~80 features in 20 sessions
```

**Why completion rate decreases:**
- Early: Simple foundational features
- Middle: More complex features, increased integration testing
- Late: Final polish, debugging, optimization

### Pattern B: Session Velocity Metrics
```
Session 1: Initialization (setup)
Sessions 2-4: High velocity (7-8 features) - foundational
Sessions 5-12: Medium velocity (5-6 features) - core work
Sessions 13+: Lower velocity (2-3 features) - complexity increases
```

### Pattern C: Baseline Health
```
Sessions 1-3: Baseline should always PASS
Sessions 4-8: Baseline PASS 95%+ of time
Sessions 9+: Occasional failures (1-2 per 10 sessions)
             → Fixed before moving forward
```

---

## Progress Tracking Templates

### Daily Standup Template
```
PROJECT: [name]
DATE: [date]

COMPLETED TODAY:
- Session 8: Features 045-047 (Chat History UI)
  Status: COMPLETE ✓

IN PROGRESS:
- Session 9 (Starting next): API Integration

BLOCKERS:
- None

METRICS:
- Features complete: 47/200 (23.5%)
- Estimated completion: Session 25
- Baseline health: PASS ✓

NOTES:
- Implementation ahead of schedule
- Consider adding more features if time permits
```

### Weekly Summary Template
```
WEEK 1 SUMMARY: Dec 9-13, 2024

PROJECT: Trading Pipeline

SESSIONS COMPLETED: 7
FEATURES IMPLEMENTED: 42 / 180 (23%)

PROGRESS BY PHASE:
- Data Pipeline: 8/12 complete (67%)
- Analysis: 12/15 complete (80%)
- ML Models: 22/50 in progress (44%)

VELOCITY:
- Average: 6 features/session
- Range: 5-8 features
- Trend: Consistent

BLOCKERS:
- None major
- Minor: Performance optimization in data loading

QUALITY METRICS:
- Baseline tests: 100% passing
- Code review: No issues
- Test coverage: 87%

RISKS & MITIGATIONS:
- ML phase may take longer
  → Consider adding buffer sessions

NEXT WEEK FOCUS:
- Complete ML models (sessions 8-12)
- Begin backtesting framework

STATUS: ON TRACK ✓
```

---

## Failure Mode Prevention Checklist

### Before Each Session
- [ ] Run baseline tests to verify starting state
- [ ] Read progress file to understand history
- [ ] Check git log to see recent commits
- [ ] Review features.json for next work item

### During Session
- [ ] Work on ONE feature (or feature group)
- [ ] Test thoroughly before marking complete
- [ ] Don't skip testing ("I'm sure it works")
- [ ] Commit frequently
- [ ] Keep code clean and documented

### After Session
- [ ] Run baseline tests again (must pass!)
- [ ] Update features.json with completion status
- [ ] Create git commit with clear message
- [ ] Add entry to claude-progress.txt
- [ ] Provide explicit guidance for next session

---

## Common Issues & Solutions

### Issue 1: Velocity Decreases Rapidly
**Cause:** Features becoming too complex
**Solution:** Break features into smaller tasks, ask for help, extend timeline

### Issue 2: Baseline Tests Fail
**Cause:** Change broke existing functionality
**Solution:** Revert last commit, debug carefully, test before re-committing

### Issue 3: Features Marked Complete But Broken
**Cause:** Insufficient testing
**Solution:** Implement stronger test requirements, always verify end-to-end

### Issue 4: Lost Context Between Sessions
**Cause:** Progress file not detailed enough
**Solution:** Add more detail to progress file, use more git commits

---

## Tools for Multi-Session Projects

### Git Commands
```bash
git log --oneline -20          # See recent commits
git diff HEAD~5                # See what changed
git revert HEAD                # Undo last commit
git reset --hard <commit>      # Go back to specific state
```

### Testing
```bash
pytest tests/baseline_test.py  # Run baseline
pytest tests/ -v               # Run all tests
pytest tests/ --lf             # Run last failed
```

### Project Management
```bash
cat features.json | grep '"passes": false' | wc -l  # Count remaining
cat claude-progress.txt | tail -50                   # See recent sessions
```

---

## Success Indicators for Multi-Session Projects

✅ **Velocity:** 3-7 features per session (project-dependent)
✅ **Quality:** Baseline tests 95%+ pass rate
✅ **Progress:** 20-30% complete by midpoint
✅ **Documentation:** Progress file updated each session
✅ **Code:** Clean, well-committed code
✅ **Testing:** Thorough end-to-end testing
✅ **Handoff:** Clear guidance for next session

---

## Summary

**Multi-session workflows enable:**
- ✅ Complex projects (1-3 month timelines)
- ✅ Large codebases (10k+ lines)
- ✅ Team collaboration (different agents)
- ✅ Progress visibility
- ✅ Quality maintenance
- ✅ Risk mitigation

**Key to success:**
- Structured initialization
- Clear feature specification
- Consistent testing
- Meticulous documentation
- Disciplined hand-offs

**Based on Anthropic's long-running agent research.**
