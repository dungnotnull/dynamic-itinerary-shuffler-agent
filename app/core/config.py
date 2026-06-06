import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # API Keys
    openweathermap_api_key: str = os.getenv("OPENWEATHERMAP_API_KEY", "")
    google_maps_api_key: str = os.getenv("GOOGLE_MAPS_API_KEY", "")
    foursquare_api_key: str = os.getenv("FOURSQUARE_API_KEY", "")
    anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

    class Config:
        env_file = ".env"

settings = Settings()
