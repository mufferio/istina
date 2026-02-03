"""
Mock provider for analysis.

Purpose:
- Provide predictable, fast analysis results without external APIs.
- Used for:
  - tests
  - offline development
  - demo flows

Behavior:
- Generates BiasScore using simple heuristics:
  - “loaded language” detection via keyword list
  - trivial claim extraction or stub claims
- Always returns the same result for the same Article id (deterministic).
"""
