from src.config.logger import *
from telegram import Update
import asyncio
import json
from collections import defaultdict
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from pathlib import Path
import os

from src.config.config import settings
from src.ai.models.ai_messages import ChatMessage
from src.ai.llm_wrapper import LLMWrapper
from src.ai.whisper_wrapper import WhisperWrapper
from src.ai.prompts import mtrack_prompt, mtrack_modify_transaction_prompt
from src.db.models.expense import Expense
from src.db.models.primary_secondary_category import PrimarySecondaryCategory
from src.db.manager import MTrackDB


logger = logging.getLogger(__name__)


class MTrackBot:
    def __init__(self, whisper: WhisperWrapper, llm: LLMWrapper, db_manager: MTrackDB):
        logger.info("Initializing MTrackBot...")
        self.__whisper = whisper
        self.__llm = llm
        self.__db_manager = db_manager
        Path(settings.voice_recording_download_path).mkdir(parents=True, exist_ok=True)
        
        self.__app = Application.builder().token(settings.telegram_bot_token).build()
        self.__app.add_handler(CommandHandler("start", self.__start))
        logger.debug("Added /start command handler.")

        self.__app.add_handlers([CommandHandler("ok", self.__handle_save), CommandHandler("save", self.__handle_save)])
        logger.debug("Added /save or /ok command handler.")

        self.__app.add_handlers([CommandHandler("list", self.__handle_list_config), CommandHandler("config", self.__handle_list_config)])
        
        self.__app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.__handle_text))
        logger.debug("Added text message handler.")
        
        self.__app.add_handler(MessageHandler(filters.VOICE, self.__handle_voice))
        logger.debug("Added voice message handler.")

        self.__app.add_handler(CommandHandler("summary", self.__handle_summary))
        logger.debug("Added summary command handler.")
        
        self.__app.add_error_handler(self.__error_handler)
        logger.debug("Added error handler.")
        logger.info("MTrackBot initialized successfully.")
        
        # Add shutdown event
        self._shutdown_event = asyncio.Event()
        

    async def run(self):
        """Run the bot with proper graceful shutdown handling."""
        logger.info("Starting MTrackBot...")
        
        try:
            # Initialize the application
            await self.__app.initialize()
            await self.__app.start()
            
            # Start polling
            logger.info("Bot is now polling for updates...")
            await self.__app.updater.start_polling(allowed_updates=Update.ALL_TYPES)
            
            # Wait for shutdown signal
            await self._shutdown_event.wait()
            
        except Exception as e:
            logger.error(f"Error in bot run: {e}")
            raise
        finally:
            # Graceful shutdown
            logger.info("Shutting down MTrackBot...")
            try:
                await self.__app.updater.stop()
                await self.__app.stop()
                await self.__app.shutdown()
                logger.info("MTrackBot shutdown complete.")
            except Exception as e:
                logger.error(f"Error during shutdown: {e}")
    

    async def stop(self):
        """Signal the bot to stop."""
        logger.info("Stop signal received.")
        self._shutdown_event.set()
    

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
       

    async def __error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
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
    

    async def __manage_transactions(self, user_msg: str, replied_to: str | None) -> str:
        categories = await self.__db_manager.get_all_primary_secondary_mappings()
        if replied_to:
            prompt = mtrack_modify_transaction_prompt(categories=categories)
            msg = [
                ChatMessage(role="assistant", content=replied_to),
                ChatMessage(role="user", content=user_msg)
            ]
        else:
            prompt = mtrack_prompt(categories=categories)
            msg = user_msg
            
        logger.debug(f"Generated prompt for LLM...")
        transactions_json = await self.__llm.ainvoke(prompt=prompt, messages=msg)
        return transactions_json
    

    async def __handle_save(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await self.__check_auth(update)
        
        replied_to = update.message.reply_to_message
        replied_to = replied_to.text if replied_to else ""
        
        if not replied_to:
            await update.message.reply_text("Please reply to a message containing transaction data to save it.")
            return
        
        json_raw = json.loads(replied_to)
        if isinstance(json_raw, list):
            expenses = [Expense.from_json(item) for item in json_raw]
        else:
            expenses = [Expense.from_json(json_raw)] 
        
        for exp in expenses:
            logger.debug(f"Prepared to save expense: {exp}")
            await self.__db_manager.add_expense(exp.to_dict())
        await update.message.reply_text(f"✅ Saved {len(expenses)} expense(s) successfully.")


    async def __handle_list_config(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await self.__check_auth(update)
      
        cards = await self.__db_manager.get_all_card_accounts()
        formatted_cards = "💳 Cards Account:\n" + "\n".join([card.to_msg() for card in cards]) 

        categories = await self.__db_manager.get_all_primary_secondary_mappings()
        formatted_categories = "🏷️ Categories:\n" + PrimarySecondaryCategory.to_msg(categories)

        await update.message.reply_text(f"{formatted_cards}\n{formatted_categories}")
    

    async def __handle_summary(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await self.__check_auth(update)

        args = context.args
        ym = args[0] if args else None  # e.g. "/summary 2025-10"

        if ym:
            year, month = map(int, ym.split("-"))
            expenses = await self.__db_manager.get_all_expenses(year=year, month=month)
        else:
            expenses = await self.__db_manager.get_all_expenses()  # current month

        text = self.build_month_summary(expenses)
        await update.message.reply_text(text)


    def build_month_summary(self, expenses: list[Expense]) -> str:
        """Build a summary message for a list of expenses."""
        if not expenses:
            return "📭 No expenses found for this month."

        total = 0.0
        total_by_card = defaultdict(float)
        total_by_category = defaultdict(float)

        # Aggregate data
        for exp in expenses:
            effective = exp.amount - exp.reimbursed
            total += effective
            total_by_card[exp.card_account] += exp.amount  # raw spend per card
            total_by_category[exp.primary_category] += effective

        # 🧾 Build Telegram message
        lines = []
        lines.append("📊 *Monthly Summary*")
        lines.append(f"Total spent: *{total:.2f}*")

        # By card
        lines.append("\n💳 *By Card*")
        for card, amt in sorted(total_by_card.items(), key=lambda x: x[1], reverse=True):
            lines.append(f"• `{card}` → {amt:.2f}")

        # By category
        lines.append("\n🏷️ *By Category*")
        for cat, amt in sorted(total_by_category.items(), key=lambda x: x[1], reverse=True):
            lines.append(f"• {cat} → {amt:.2f}")

        return "\n".join(lines)