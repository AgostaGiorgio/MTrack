from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide
from src.di import Container

from src.models.transactions import Transaction


api_router = APIRouter()

@api_router.get("", response_model=list[Transaction], status_code=200)
@inject
async def get_transactions() -> list[Transaction]:
    pass