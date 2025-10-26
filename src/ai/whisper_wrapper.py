from src.config.logger import *
import torch 
import os
import whisper

from src.config.config import settings


logger = logging.getLogger(__name__)


class WhisperWrapper:
    def __init__(self):
        self.__model = None
        self.__device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Whisper running using device: {self.__device}")
        
        self.__load_model()
        
    def __load_model(self):
        if self.__model is None:
            logger.debug(f"Loading Whisper {settings.whisper_model_size} model...")
            
            os.makedirs(settings.whisper_model_download_path, exist_ok=True)

            self.__model = whisper.load_model(
                settings.whisper_model_size, 
                device=self.__device,
                download_root=settings.whisper_model_download_path
            )
            logger.debug(f"Whisper model loaded successfully from {settings.whisper_model_download_path}.")
            
    async def transcribe(self, audio_path: str, language: str = "it") -> str:
        logger.debug(f"Transcribing audio file: {audio_path}")
        try:
            result = self.__model.transcribe(
                audio_path,
                language=language,
                fp16=(self.__device == "cuda"),
                verbose=False
            )
            transcription = result.get("text", "")
            logger.debug(f"Transcription completed.")
            return transcription
        except Exception as e:
            logger.error(f"Error during transcription: {e}")
            return ""
        
        
            
            
            
            