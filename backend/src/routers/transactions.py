from fastapi import APIRouter, Depends, Query
from dependency_injector.wiring import inject, Provide
from uuid import UUID
from typing import Optional
from src.di import Container

from src.routers.pojos.transactions import UpdateTransactionCategories
from src.models.transactions import Transaction
from src.services.transactions import TransactionsService


api_router = APIRouter()

@api_router.get("", response_model=list[Transaction], status_code=200)
@inject
async def get_transactions(
    year: Optional[int] = Query(None, description="Year for MTrack month"),
    month: Optional[int] = Query(None, description="Month for MTrack month (1-12)"),
    transactions_service: TransactionsService = Depends(Provide[Container.transactions_service])
) -> list[Transaction]:
    return await transactions_service.get_transactions(year=year, month=month)

@api_router.put("/{transaction_id}", response_model=Transaction, status_code=200)
@inject
async def update_transaction_categories(
    transaction_id: UUID,
    categories_update: UpdateTransactionCategories,
    transactions_service: TransactionsService = Depends(Provide[Container.transactions_service])
) -> Transaction:
    return await transactions_service.update_transaction_categories(
        transaction_id=transaction_id,
        primary_category_id=categories_update.primary_category_id,
        secondary_category_id=categories_update.secondary_category_id
    )