import logging
from datetime import datetime
from src.utils.date_utils import get_mtrack_month
from src.repositories.dashboard import DashboardRepository
from src.models.dashboard import DashboardData

logger = logging.getLogger(__name__)

class DashboardService:
    def __init__(self, dashboard_repository: DashboardRepository):
        self.__dashboard_repository = dashboard_repository

    async def get_dashboard_data(self) -> DashboardData:
        logger.info("Fetching dashboard data...")
        
        card_summaries = await self.__dashboard_repository.get_card_summaries()
        categories_summary = await self.__dashboard_repository.get_categories_summary()
        monthly_trends = await self.__dashboard_repository.get_monthly_trends()
        return DashboardData(
            current_month=get_mtrack_month(datetime.now()),
            total_spent=sum(card.amount for card in card_summaries),
            cards_summary=card_summaries,
            categories_summary=categories_summary,
            monthly_trends=monthly_trends
        )