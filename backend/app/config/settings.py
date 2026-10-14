from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Company Brain"
    environment: str = "development"
    api_prefix: str = "/api"
    frontend_origin: str = "http://localhost:5173"
    falkordb_url: str = "redis://localhost:6379"
    falkordb_graph: str = "company_brain"
    github_webhook_secret: str | None = None
    slack_signing_secret: str | None = None
    llm_provider: str = "stub"
    llm_model: str = "local-grounded"

    model_config = SettingsConfigDict(env_file=".env", env_prefix="", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
