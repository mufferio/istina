"""
AnalysisService (use case).

Workflow:
1) Select which Articles to analyze (unscored or filtered by params).
2) For each Article:
   - Run ScoringVisitor/Provider to produce BiasScore
   - Persist BiasScore via repository
3) Return summary stats + failures.

Reliability:
- Uses retry + rate limiting around provider calls.
- Handles provider failures gracefully (log and continue or stop based on config).
"""
