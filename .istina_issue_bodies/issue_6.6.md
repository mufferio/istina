## Goal
Create the structure for Gemini integration without relying on perfect parsing yet

## Tasks
- [ ] create src/model/providers/gemini_provider.py
- [ ] read GEMINI_API_KEY from Settings
- [ ] define prompt templates for:
  - [ ] bias detection + rhetorical flags
  - [ ] claim extraction + verdict scaffolding
- [ ] implement a call wrapper function (no parsing perfection required yet)
- [ ] ensure secrets never logged

## Verify
Provider can be instantiated when API key exists (without crashing)

## Done when
GeminiProvider skeleton is ready for parsing + normalization
