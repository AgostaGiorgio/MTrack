import asyncio
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
    await bot.run()

    
if __name__ == "__main__":
    asyncio.run(main())