"""
AnalyzeCommand.

Purpose:
- Implement: "istina analyze [--since ...] [--limit N] [--provider ...]"
- Calls AnalysisService to:
  - select Articles needing analysis
  - run provider/visitor
  - persist BiasScores

Output:
- Returns analysis results stats and any errors encountered
"""
