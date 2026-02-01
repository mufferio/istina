"""
Provider interface (AI analysis contract).

Defines:
- A standard method signature like:
  - analyze_article(article: Article) -> BiasScore

Design goals:
- Services depend on this interface, not on Gemini/OpenAI/etc.
- Normalize provider outputs into BiasScore (provider-agnostic).

Notes:
- Handle provider errors with domain-level exceptions
  (or raise custom exceptions used by services).
"""
