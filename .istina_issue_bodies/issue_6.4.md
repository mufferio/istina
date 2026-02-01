## Goal
Instantiate the correct provider based on configuration

## Tasks
- [ ] create src/model/providers/provider_factory.py
- [ ] implement create_provider(settings) -> BaseProvider
- [ ] support: mock, gemini
- [ ] invalid provider raises ConfigError

## Verify
Switch ISTINA_PROVIDER=mock uses MockProvider instance

## Done when
Provider can be swapped by env change only
