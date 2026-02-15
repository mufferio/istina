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


class ConfigError(ValueError):
    """Raised when Istina configuration is invalid."""
    pass


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

def validate_settings(settings: Settings):
    """
    Validate settings values to ensure they are within expected parameters.
    This can help catch misconfigurations early.
    """

    valid_envs = {"dev", "test", "prod"}
    valid_providers = {"mock", "openai", "azure", "gemini"}
    valid_repo_types = {"memory", "file"}

    if settings.env not in valid_envs:
        raise ConfigError(f"Invalid env: {settings.env}. Must be one of {valid_envs}")

    if settings.provider not in valid_providers:
        raise ConfigError(f"Invalid provider: {settings.provider}. Must be one of {valid_providers}")
    
    if settings.repo_type not in valid_repo_types:
        raise ConfigError(f"Invalid repo_type: {settings.repo_type}. Must be one of {valid_repo_types}")
