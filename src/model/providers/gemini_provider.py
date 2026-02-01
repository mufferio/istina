"""
Gemini provider implementation.

Purpose:
- Real AI-backed analysis using Google Gemini API.

Responsibilities:
- Build prompts for:
  - claim extraction + fact-check verdict scaffolding
  - rhetorical bias detection and structured scoring
- Call Gemini SDK/HTTP
- Parse/validate the model response
- Normalize output into BiasScore
- Enforce rate limiting + retries (use utils/rate_limiter.py and utils/retry.py)

Important:
- Keep prompts versioned and test parsing heavily.
- Always handle malformed outputs safely (fallback to “insufficient evidence”).
- Never leak API keys into logs.
"""
