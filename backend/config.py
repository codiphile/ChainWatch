from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    openai_api_key: str = ""
    news_api_key: str = ""
    openweather_api_key: str = ""
    backend_url: str = "http://localhost:8000"

    # Demo regions with coordinates
    regions: dict = {
        "Shanghai": {"lat": 31.2304, "lon": 121.4737, "port": "Shanghai Port"},
        "Rotterdam": {"lat": 51.9225, "lon": 4.4792, "port": "Port of Rotterdam"},
        "Los Angeles": {"lat": 33.7405, "lon": -118.2760, "port": "Port of Los Angeles"},
    }

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
