from dependency_injector import containers, providers
from src.config.config import settings

from src.ai.llm_wrapper import LLMWrapper
from src.ai.whisper_wrapper import WhisperWrapper
from src.bot.mtrack_bot import MTrackBot

class DIContainer(containers.DeclarativeContainer):
    whisper = providers.Singleton(WhisperWrapper)
    llm = providers.Singleton(LLMWrapper, llm_url=settings.llm_url, model=settings.llm_model)
    mtrack_bot = providers.Singleton(MTrackBot, whisper=whisper, llm=llm)