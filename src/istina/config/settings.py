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
from dotenv import load_dotenv
import os


ALLOWED_ENVS = {}
ALLOWED_PROVIDERS = {}



@dataclass
class Settings:
    """
    Central configuration object for the Istina app.
    """

    env: str = "dev"
    provider: str = "mock"
    repo_type: str = "memory"
    log_level: str = "INFO"
    data_dir: str = "./data"
    rate_limit_rpm: int = 60


def load_settings() -> Settings:
    """
    Load settings from:
    1. defaults (dataclass)
    2. .env file
    3. system environment variables

    Order of precedence:
    env vars > .env > defaults
    """

    # 🔑 this loads .env automatically
    load_dotenv()

    return Settings(
        env=os.getenv("ISTINA_ENV", "dev"),
        provider=os.getenv("ISTINA_PROVIDER", "mock"),
        repo_type=os.getenv("ISTINA_REPO_TYPE", "memory"),
        log_level=os.getenv("ISTINA_LOG_LEVEL", "INFO"),
        data_dir=os.getenv("ISTINA_DATA_DIR", "./data"),
        rate_limit_rpm=int(os.getenv("ISTINA_RATE_LIMIT_RPM", "60")),
    )

