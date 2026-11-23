from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Equipment Monitoring API"
    database_url: str = "sqlite:///./equipment.db"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
