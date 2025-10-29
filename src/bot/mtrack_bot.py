from src.config.logger import *
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from pathlib import Path
import os

from src.config.config import settings
from src.ai.models.ai_messages import ChatMessage
from src.ai.llm_wrapper import LLMWrapper
from src.ai.whisper_wrapper import WhisperWrapper
from src.ai.prompts import mtrack_prompt, mtrack_modify_transaction_prompt


logger = logging.getLogger(__name__)


class MTrackBot:
    def __init__(self, whisper: WhisperWrapper, llm: LLMWrapper):
        logger.info("Initializing MTrackBot...")
        self.__whisper = whisper
        self.__llm = llm
        Path(settings.voice_recording_download_path).mkdir(parents=True, exist_ok=True)
        
        self.__app = Application.builder().token(settings.telegram_bot_token).build()
        self.__app.add_handler(CommandHandler("start", self.__start))
        logger.debug("Added /start command handler.")
        self.__app.add_handler(CommandHandler("ok", self.__handle_save))
        self.__app.add_handler(CommandHandler("save", self.__handle_save))
        logger.debug("Added /save or /ok command handler.")
        self.__app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.__handle_text))
        logger.debug("Added text message handler.")
        self.__app.add_handler(MessageHandler(filters.VOICE, self.__handle_voice))
        logger.debug("Added voice message handler.")
        self.__app.add_error_handler(self.error_handler)
        logger.debug("Added error handler.")
        logger.info("MTrackBot initialized successfully.")
        
    async def run(self):
        logger.info("Starting MTrackBot...")
        await self.__app.initialize()
        await self.__app.start()
        await self.__app.run_polling(allowed_updates=Update.ALL_TYPES)

    async def stop(self):
        await self.__app.updater.stop()
        await self.__app.stop()
        await self.__app.shutdown()
    
    async def __check_auth(self, update: Update) -> bool:
        """Check if user is authorized"""
        chat_id = update.effective_chat.id
        if chat_id != settings.telegram_chat_id:
            logger.warning(f"Unauthorized access attempt from chat_id: {chat_id}")
            await update.message.reply_text("⛔ Sorry, you are not authorized to use this bot.")
            return
    
    async def __start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await self.__check_auth(update)
        
        await update.message.reply_text(
            'Hi! I can handle text messages and voice recordings.\n'
            'Send me a text message or a voice note!'
        )
       
    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        logger.error(f"Exception while handling an update: {context.error}")

    async def __handle_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await self.__check_auth(update)
        
        user_text = update.message.text
        replied_to = update.message.reply_to_message
        replied_to = replied_to.text if replied_to else ""
        
        transactions_json = await self.__manage_transactions(
            user_msg=user_text,
            replied_to=replied_to
        )
        
        await update.message.reply_text(transactions_json)
        
    async def __handle_voice(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await self.__check_auth(update)
        
        voice = update.message.voice
        user_id = update.effective_user.id
        
        logger.info(f"Received voice from {user_id}, duration: {voice.duration}s")
        
        # Download the voice file
        file = await context.bot.get_file(voice.file_id)
        filename = f"voice_{user_id}_{voice.file_unique_id}.ogg"
        filepath = os.path.join(settings.voice_recording_download_path, filename)
        await file.download_to_drive(filepath)        
        logger.debug(f"Voice saved to: {filepath}")

        logger.debug("Starting transcription...")
        transcription = await self.__whisper.transcribe(filepath, language="it")
        logger.debug("Transcription completed.")
        
        replied_to = update.message.reply_to_message
        replied_to = replied_to.text if replied_to else ""
        
        transactions_json = await self.__manage_transactions(
            user_msg=transcription,
            replied_to=replied_to
        )
        
        await update.message.reply_text(transactions_json)
        
    async def __handle_save(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await self.__check_auth(update)
        
        replied_to = update.message.reply_to_message
        replied_to = replied_to.text if replied_to else ""
        
        if not replied_to:
            await update.message.reply_text("Please reply to a message containing transaction data to save it.")
            return
        
        await update.message.reply_text("Save functionality is not implemented yet.")
        
    async def __manage_transactions(self, user_msg: str, replied_to: str | None) -> str:
        if replied_to:
            prompt = mtrack_modify_transaction_prompt()
            msg = [
                ChatMessage(role="assistant", content=replied_to),
                ChatMessage(role="user", content=user_msg)
            ]
        else:
            prompt = mtrack_prompt()
            msg = user_msg
            
        logger.debug(f"Generated prompt for LLM...")
        transactions_json = await self.__llm.ainvoke(prompt=prompt, messages=msg)
        return transactions_json