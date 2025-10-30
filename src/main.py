import asyncio
import signal
from src.config.logger import *
from src.utils.health_server import start_health_server

from src.di import DIContainer

logger = logging.getLogger(__name__)


async def main():
    start_health_server(port=8080)

    containter = DIContainer()
    db_manager = containter.db_manager()
    bot = containter.mtrack_bot()

    await db_manager.initialize()
    
    loop = asyncio.get_running_loop()
    
    def signal_handler(signum, frame):
        logger.info(f"Received signal {signum}, initiating shutdown...")
        asyncio.create_task(bot.stop())
    
    # Register signal handlers
    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, lambda s=sig: asyncio.create_task(bot.stop()))
    
    try:
        # Run the bot
        await bot.run()
    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt received, shutting down...")
    finally:
        # Cleanup database connection
        await db_manager.close()
        logger.info("Shutdown complete.")

    
if __name__ == "__main__":
    asyncio.run(main())