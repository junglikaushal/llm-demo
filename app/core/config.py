from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "LLM Demo"
    openai_api_key: str  # no default — app refuses to start without it
    openai_model: str = "gpt-4o-mini"
    request_timeout: float = 30.0

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
