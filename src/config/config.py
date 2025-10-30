from pydantic_settings import BaseSettings
from typing import Literal

class Settings(BaseSettings):
    telegram_bot_token: str
    telegram_chat_id: int
    
    voice_recording_download_path: str

    whisper_model_download_path: str    
    whisper_model_size: Literal["tiny", "base", "small", "medium", "large"] = "small"
    
    llm_url: str
    llm_model: str

    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: str
    postgres_database: str
    
    mtrack_categories: list[str] = []
    mtrack_primary_secondary_categories: list[tuple[str, str]] = []
    mtrack_card_accounts: list[str] = []

    class Config:
        env_file = ".env"

settings = Settings()

