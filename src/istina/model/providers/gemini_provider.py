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
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable, Dict, Optional

import httpx

from istina.model.entities.article import Article
from istina.model.entities.bias_score import BiasScore
from istina.model.providers.base_provider import BaseProvider
from istina.utils.rate_limiter import RateLimiter, maybe_acquire
from istina.utils.retry import retry 



class ProviderError(RuntimeError):
    """Raised when the provider call fails (network/status/etc.)."""


def _get_setting(settings: Any, key: str, default: Any = None) -> Any:
    if settings is None:
        return default
    if isinstance(settings, dict):
        return settings.get(key, default)
    if hasattr(settings, key):
        return getattr(settings, key)
    get = getattr(settings, "get", None)
    if callable(get):
        return get(key, default)
    return default


def build_bias_prompt(article: Article) -> str:
    """
    Prompt template: bias detection + rhetorical flags.

    Output requirements (we'll parse later):
      - overall_bias_label: left|center|right|unknown
      - rhetorical_flags: list[str]
      - confidence: float 0..1
      - short justification
    """
    title = getattr(article, "title", "") or ""
    summary = getattr(article, "summary", "") or ""
    source = getattr(article, "source", "") or ""
    url = getattr(article, "url", "") or ""

    return f"""
You are Istina, an expert media bias analyst. Analyze the following news article for political bias and rhetorical manipulation techniques.

Article to analyze:
Source: {source}
Title: {title}
Summary: {summary}
URL: {url}

Analysis framework:

1. OVERALL BIAS CLASSIFICATION:
   - Determine if the article leans left, center, right, or unknown
   - Base assessment on:
     * Word choice and framing
     * Selection and omission of facts
     * Sources cited or ignored
     * Contextual emphasis

2. RHETORICAL FLAGS DETECTION:
   Identify any of these manipulation techniques present:
   - loaded_language: Emotionally charged words intended to influence
   - cherry_picking: Selective presentation of facts
   - ad_hominem: Attacking person rather than argument
   - appeal_to_fear: Using fear to influence opinion
   - strawman: Misrepresenting opposing viewpoint
   - whataboutism: Deflecting by pointing to other issues
   - false_dilemma: Presenting only two options when more exist
   - us_vs_them: Creating artificial divisions
   - assertion_without_evidence: Making claims without support
   - sensationalism: Exaggerating for dramatic effect

3. CONFIDENCE ASSESSMENT:
   - Rate your confidence in this analysis from 0.0 (uncertain) to 1.0 (very confident)
   - Consider article length, clarity, and available context

Return ONLY a valid JSON object with this exact structure:
{{
  "overall_bias_label": "left|center|right|unknown",
  "rhetorical_flags": ["flag1", "flag2"],
  "confidence": 0.0,
  "justification": "Brief explanation of your assessment"
}}
""".strip()


def build_claims_prompt(article: Article) -> str:
    """
    Prompt template: claim extraction + verdict scaffolding.

    Output requirements (we'll parse later):
      - claim_checks: list of objects with {claim, verdict, confidence, evidence}
    """
    title = getattr(article, "title", "") or ""
    summary = getattr(article, "summary", "") or ""
    source = getattr(article, "source", "") or ""
    url = getattr(article, "url", "") or ""

    return f"""
You are Istina, a fact-checking and claim verification expert. Extract and assess factual claims from the following news article.

Article to analyze:
Source: {source}
Title: {title}
Summary: {summary}
URL: {url}

Task: Extract up to 5 concrete, verifiable factual claims and provide preliminary assessment.

Claim extraction criteria:
- Focus on specific, verifiable assertions:
  * Numerical data (statistics, amounts, dates, quantities)
  * Attribution claims ("X said Y", "According to Z")
  * Causal relationships ("A caused B")
  * Event descriptions ("X happened on Y date")
  * Timeline assertions ("before/after X")
- Exclude opinions, predictions, or subjective statements
- If summary lacks detail, extract fewer claims rather than speculating

Verdict categories:
- "true": Claim appears accurate based on available information
- "false": Claim appears inaccurate or misleading
- "mixed": Claim is partially true/false or needs important context
- "unverified": Cannot assess without additional evidence (default for this phase)

Confidence scale:
- 0.0-0.3: Low confidence, substantial uncertainty
- 0.4-0.6: Moderate confidence, some uncertainty
- 0.7-1.0: High confidence, minimal uncertainty

Return ONLY a valid JSON object with this exact structure:
{{
  "claim_checks": [
    {{
      "claim": "Specific factual claim extracted from article",
      "verdict": "unverified",
      "confidence": 0.0,
      "evidence": ["Supporting information if available", "Context or caveats"]
    }}
  ]
}}
""".strip()


@dataclass
class GeminiProvider(BaseProvider):
    """
    Gemini provider scaffold.

    v0 behavior:
      - calls Gemini generateContent with prompts
      - does NOT require perfect parsing yet (stores raw_response)
      - returns a normalized BiasScore with conservative defaults (unknown/empty)
    """

    api_key: str = field(repr=False)
    model: str = "gemini-1.5-pro"
    timeout_seconds: float = 10.0
    limiter: Optional[RateLimiter] = None

    # For testability: allow injection of a request function
    _post: Optional[Callable[..., httpx.Response]] = field(default=None, repr=False)

    @classmethod
    def from_settings(cls, settings: Any, *, limiter: Optional[RateLimiter] = None) -> "GeminiProvider":
        api_key = _get_setting(settings, "gemini_api_key", None)
        model = _get_setting(settings, "gemini_model", "gemini-1.5-pro")
        if not api_key:
            raise ValueError("gemini_api_key is required to instantiate GeminiProvider")
        return cls(api_key=str(api_key), model=str(model), limiter=limiter)

    def analyze_article(self, article: Article) -> BiasScore:
        aid = getattr(article, "id", None)
        if not aid:
            raise ValueError("Article missing id")

        # Build prompts (v0: two calls; later you can merge into one if desired)
        bias_prompt = build_bias_prompt(article)
        claims_prompt = build_claims_prompt(article)

        # Call provider (no perfect parsing required yet)
        bias_raw = self._call_gemini(bias_prompt)
        claims_raw = self._call_gemini(claims_prompt)

        # v0: conservative normalized output (until parser/normalizer issue)
        # Store raw_response for debugging/auditing; NEVER include api key.
        raw_response: Dict[str, Any] = {
            "bias_call": bias_raw,
            "claims_call": claims_raw,
            "model": self.model,
        }

        # If you want minimal extraction now, keep it extremely defensive:
        overall = "unknown"
        rhetorical_flags = []
        claim_checks = []
        confidence = 0.0

        # Timestamp should reflect analysis time (not deterministic like MockProvider)
        timestamp = datetime.now(timezone.utc)

        return BiasScore(
            article_id=aid,
            provider="gemini",
            overall_bias_label=overall,
            rhetorical_bias=rhetorical_flags,
            claim_checks=claim_checks,
            confidence=confidence,
            timestamp=timestamp,
            raw_response=raw_response,
        )

    def _call_gemini(self, prompt: str) -> Dict[str, Any]:
        """
        Wrapper for Gemini call.
        - Applies optional rate limiting + retry for transient network issues.
        - Does NOT log secrets.
        - Returns parsed JSON response payload (dict) from HTTP call (raw).
        """
        maybe_acquire(self.limiter)

        def _do_call() -> Dict[str, Any]:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent"
            params = {"key": self.api_key}  # Do not log this.
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
            }

            post = self._post
            if post is None:
                with httpx.Client(timeout=self.timeout_seconds) as client:
                    resp = client.post(url, params=params, json=payload)
            else:
                resp = post(url, params=params, json=payload, timeout=self.timeout_seconds)

            if resp.status_code != 200:
                # Never include URL with key, API key, or response body in the message.
                raise ProviderError(f"Gemini API returned status {resp.status_code}")

            try:
                response_data = resp.json()
                # Sanitize response data to ensure no secrets are accidentally logged
                if isinstance(response_data, dict) and "key" in str(response_data):
                    # Remove any potential API key leaks in response
                    response_data = {k: v for k, v in response_data.items() 
                                   if k not in ("key", "api_key", "apiKey")}
                return response_data
            except Exception as e:
                raise ProviderError(f"Gemini returned invalid JSON response") from e

        # Retry only on network-ish exceptions + ProviderError
        return retry(
            _do_call,
            exceptions=(httpx.TimeoutException, httpx.NetworkError, ProviderError),
            max_attempts=3,
            base_delay=0.5,
            backoff_factor=2.0,
        )