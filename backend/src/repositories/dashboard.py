import logging
from src.clients.postgres_client import PostgresClient
from src.repositories import queries as q
from src.models.dashboard import CardSummary, CategorySummary, MonthlyTrend
from src.models.statistics import CategoryMonthlyTrend

logger = logging.getLogger(__name__)

class DashboardRepository:
    def __init__(self, postgres_client: PostgresClient):
        self.__postgres_client = postgres_client

    async def get_monthly_trends(self) -> list[MonthlyTrend] | None:
        logger.debug("Executing monthly trends query...")
        monthly_trends = None
        async with self.__postgres_client.async_session() as session:
            try:
                result = await session.execute(q.GET_MONTHLY_TRENDS)
                rows = result.mappings().all()
                monthly_trends = [MonthlyTrend(**row) for row in rows]
                logger.debug(f"Monthly trends data retrieved!")
            except Exception as e:
                logger.error(f"Error fetching monthly trends data", exc_info=e)
        return monthly_trends

    async def get_categories_summary(self) -> list[CategorySummary] | None:
        logger.debug("Executing categories summary query...")
        categories_summary = None
        async with self.__postgres_client.async_session() as session:
            try:
                result = await session.execute(q.GET_CATEGORIES_SUMMARY)
                rows = result.mappings().all()
                categories_summary = [CategorySummary(**row) for row in rows]
                logger.debug(f"Categories summary data retrieved!")
            except Exception as e:
                logger.error(f"Error fetching categories summary data", exc_info=e)
            
            for category in categories_summary:
                logger.debug(f"Getting subcategories for Category: {category.name}...")
                try:
                    result = await session.execute(q.GET_SUBCATEGORIES_SUMMARY, {"primary_id": str(category.id)})
                    sub_rows = result.mappings().all()
                    category.sub_categories = [CategorySummary(**sub_row) for sub_row in sub_rows]
                    logger.debug(f"Subcategories for Category: {category.name} retrieved!")
                except Exception as e:
                    logger.error(f"Error fetching subcategories summary data for Category: {category.name}", exc_info=e)
        return categories_summary
    
    async def get_category_monthly_trends(self, category_names: list[str]) -> list[CategoryMonthlyTrend]:
        logger.debug(f"Executing category monthly trends query for: {category_names}...")
        async with self.__postgres_client.async_session() as session:
            try:
                result = await session.execute(
                    q.GET_CATEGORY_MONTHLY_TRENDS,
                    {"category_names": [name.lower() for name in category_names]},
                )
                rows = result.mappings().all()
                grouped: dict[str, list[MonthlyTrend]] = {}
                for row in rows:
                    cat_name = row["category_name"]
                    if cat_name not in grouped:
                        grouped[cat_name] = []
                    grouped[cat_name].append(
                        MonthlyTrend(month=row["month"], amount=row["amount"])
                    )
                return [
                    CategoryMonthlyTrend(category_name=name, monthly_data=data)
                    for name, data in grouped.items()
                ]
            except Exception as e:
                logger.error(
                    f"Error fetching category monthly trends", exc_info=e
                )
                return []

    async def get_card_summaries(self) -> list[CardSummary] | None:
        logger.debug("Executing card summary query...")
        card_summaries = None
        async with self.__postgres_client.async_session() as session:
            try:
                result = await session.execute(q.GET_CARD_SUMMARIES)
                rows = result.mappings().all()
                card_summaries = [CardSummary(**row) for row in rows]
                logger.debug(f"Card summary data retrieved!")
            except Exception as e:
                logger.error(f"Error fetching card summary data", exc_info=e)
        return card_summaries