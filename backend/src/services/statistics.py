import logging
from datetime import datetime
from src.utils.date_utils import get_mtrack_month
from src.repositories.dashboard import DashboardRepository
from src.models.statistics import StatisticsData

logger = logging.getLogger(__name__)


class StatisticsService:
    def __init__(self, dashboard_repository: DashboardRepository):
        self.__dashboard_repository = dashboard_repository

    async def get_statistics(self, category_names: list[str]) -> StatisticsData:
        logger.info("Fetching statistics data...")

        card_summaries = await self.__dashboard_repository.get_card_summaries()
        total_spent = sum(card.amount for card in card_summaries) if card_summaries else 0

        monthly_trends = await self.__dashboard_repository.get_monthly_trends()
        category_trends = await self.__dashboard_repository.get_category_monthly_trends(
            category_names
        )

        return StatisticsData(
            current_month=get_mtrack_month(datetime.now()),
            total_spent=total_spent,
            monthly_trends=monthly_trends or [],
            category_trends=category_trends or [],
        )
