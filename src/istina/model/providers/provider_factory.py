"""
ProviderFactory.

Purpose:
- Central place to select and create a Provider implementation based on settings.

Inputs:
- settings.provider_name (e.g., "mock", "gemini")

Outputs:
- An instance implementing BaseProvider

Design goal:
- Switching providers should require no changes in services/controllers.
"""
