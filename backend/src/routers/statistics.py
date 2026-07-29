from fastapi import APIRouter, Depends, Query
from dependency_injector.wiring import inject, Provide
from src.di import Container

from src.models.statistics import StatisticsData
from src.services.statistics import StatisticsService


api_router = APIRouter()


@api_router.get("", response_model=StatisticsData, status_code=200)
@inject
async def get_statistics(
    categories: list[str] = Query(default=[]),
    statistics_service: StatisticsService = Depends(
        Provide[Container.statistics_service]
    ),
) -> StatisticsData:
    return await statistics_service.get_statistics(category_names=categories)
