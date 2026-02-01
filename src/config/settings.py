"""
Settings management.

Purpose:
- Load configuration from:
  - environment variables
  - .env file (dev)
  - defaults (safe baseline)

Outputs:
- A Settings object containing:
  - env (dev/test/prod)
  - log_level
  - repository type + data directory
  - provider selection + API keys
  - rate limit settings

Notes:
- Keep secrets out of logs.
- In tests, construct Settings directly rather than relying on .env.
"""
