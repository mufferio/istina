## Goal
Convert Gemini output into your normalized BiasScore schema

## Tasks
- [ ] implement robust parsing logic
- [ ] handle invalid JSON or missing fields safely
- [ ] fill BiasScore fields consistently
- [ ] fallback: “insufficient evidence” for broken claim checks

## Verify
Given a mocked Gemini response, parser returns a valid BiasScore

## Done when
GeminiProvider returns normalized, safe BiasScores reliably
