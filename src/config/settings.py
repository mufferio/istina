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
from dataclasses import dataclass

@dataclass
class Settings:
    """
    Central configuration object for the entire Istina app.

    This should be the single source of truth for:
    - environment
    - provider selection
    - repository type
    - logging level
    - data paths
    """

    env: str = "dev"
    provider: str = "mock"
    repo_type: str = "memory"
    log_level: str = "INFO"
    data_dir: str = "./data"
    rate_limit_rpm: int = 60
