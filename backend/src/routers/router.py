from fastapi import APIRouter, Depends, HTTPException, Query
from dependency_injector.wiring import inject, Provide
from src.di import Container
from uuid import UUID

from src.models.dashboard import DashboardData
from src.services.dashboard import DashboardService


api_router = APIRouter()

@api_router.get("/dashboard", response_model=DashboardData, status_code=200)
@inject
async def get_dashboard_data(dashboard_service: DashboardService = Depends(Provide[Container.dashboard_service])) -> DashboardData:
    return await dashboard_service.get_dashboard_data()