from fastapi import APIRouter, Depends, HTTPException, Query, Response
from dependency_injector.wiring import inject, Provide
from uuid import UUID
from typing import Optional
from src.di import Container

from src.routers.pojos.transactions import UpdateTransaction
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
async def update_transaction(
    transaction_id: UUID,
    transaction_update: UpdateTransaction,
    transactions_service: TransactionsService = Depends(Provide[Container.transactions_service])
) -> Transaction:
    transaction = await transactions_service.update_transaction(
        transaction_id=transaction_id,
        primary_category_id=transaction_update.primary_category_id,
        secondary_category_id=transaction_update.secondary_category_id,
        amount=transaction_update.amount,
        transaction_date=transaction_update.date,
        update_primary="primary_category_id" in transaction_update.model_fields_set,
        update_secondary="secondary_category_id" in transaction_update.model_fields_set,
        update_amount="amount" in transaction_update.model_fields_set,
        update_date="date" in transaction_update.model_fields_set and transaction_update.date is not None,
    )
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction

@api_router.delete("/{transaction_id}", status_code=204)
@inject
async def delete_transaction(
    transaction_id: UUID,
    transactions_service: TransactionsService = Depends(Provide[Container.transactions_service])
) -> Response:
    deleted = await transactions_service.delete_transaction(transaction_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return Response(status_code=204)
