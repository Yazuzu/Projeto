import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    # Discord
    DISCORD_BOT_TOKEN: str
    CREATOR_ID: int = 766317071369109544

    # Models
    MODEL_HIGH: str = "hermes3:8b"
    MODEL_MEDIUM: str = "qwen2.5:3b"
    MODEL_LOW: str = "qwen2.5:0.5b"

    # Paths
    EMOTION_LIB_PATH: Optional[str] = None

settings = Settings()
