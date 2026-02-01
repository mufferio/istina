"""
ScoringVisitor.

Purpose:
- A concrete visitor that produces BiasScore for an Article.
- Often wraps a Provider and returns normalized results.

Used by:
- analysis_service.py to apply analysis consistently across many Articles
- helps keep analysis logic modular and testable
"""
