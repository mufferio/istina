"""
Central error handling and app-level exceptions.

Purpose:
- Define custom exceptions:
  - ConfigError
  - RepositoryError
  - ProviderError
  - AdapterError
  - ValidationError
- Provide helper to format user-friendly CLI errors.

Used by:
- controller to print consistent errors without stack traces in normal mode.
"""
