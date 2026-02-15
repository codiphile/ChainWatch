from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    openai_api_key: str = ""
    news_api_key: str = ""
    openweather_api_key: str = ""
    aisstream_api_key: str = ""
    backend_url: str = "http://localhost:8000"

    # Demo regions with coordinates and port bounding boxes
    # Bounding boxes are approximately 50km radius around major ports
    regions: dict = {
        "Shanghai": {
            "lat": 31.2304,
            "lon": 121.4737,
            "port": "Shanghai Port",
            "bbox": [[30.9, 121.2], [31.5, 122.0]]  # ~50km radius
        },
        "Rotterdam": {
            "lat": 51.9225,
            "lon": 4.4792,
            "port": "Port of Rotterdam",
            "bbox": [[51.7, 4.2], [52.1, 4.8]]  # ~50km radius
        },
        "Los Angeles": {
            "lat": 33.7405,
            "lon": -118.2760,
            "port": "Port of Los Angeles",
            "bbox": [[33.5, -118.5], [33.9, -118.0]]  # ~50km radius
        },
    }

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
