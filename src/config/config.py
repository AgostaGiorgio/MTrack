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
    
    mtrack_primary_categories: list[str]
    mtrack_secondary_categories: list[str]

    class Config:
        env_file = ".env"

settings = Settings()

