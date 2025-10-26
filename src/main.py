from src.config.logger import *
from src.utils.health_server import start_health_server

from src.di import DIContainer

logger = logging.getLogger(__name__)


def main():
    containter = DIContainer()
    bot = containter.mtrack_bot()
    
    start_health_server(port=8080)
    
    bot.run()
    
if __name__ == "__main__":
    main()