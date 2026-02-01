"""
BiasScore (analysis result) entity.

Represents:
- Structured output of the AI analysis layer for an Article.

Typical fields:
- article_id
- provider_name, provider_model (optional)
- overall_bias_label (e.g., left/center/right/unknown) OR multi-axis scores
- rhetorical_bias: list of flags (loaded language, framing, etc.)
- claim_checks: list of extracted claims with:
  - claim_text
  - verdict: supported/contradicted/insufficient
  - evidence_citations: urls/snippets/quotes references
- confidence and timestamps

Rules:
- Must be serializable.
- Keep it provider-agnostic: store normalized fields, not raw provider format.
- Optionally store raw_response for auditing/debugging.
"""
