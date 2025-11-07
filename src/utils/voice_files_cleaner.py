import time
from src.config.logger import *
from src.config.config import settings
import asyncio
from pathlib import Path

logger = logging.getLogger(__name__)

async def voice_files_cleaner():
    while True:
        try:
            logger.debug("Cleaning up old voice files...")
            
            voice_folder = Path(settings.voice_recording_download_path)
            current_time = time.time()
            files_deleted = 0
            
            for file in voice_folder.iterdir():
                try:
                    if file.is_file():
                        file_age = current_time - file.stat().st_mtime
                        if file_age > 10800:  # 3 hours in seconds
                            file.unlink()
                            files_deleted += 1
                            logger.debug(f"Deleted old voice file: {file.name}")
                except Exception as e:
                    logger.error(f"Error deleting file {file.name}: {e}")
            
        except Exception as e:
            logger.error(f"Error during voice files cleanup: {e}")
            
        logger.info(f"Voice files cleanup complete. Deleted {files_deleted} files.")
        
        await asyncio.sleep(3600) # Wait for 1 hour before next cleanup