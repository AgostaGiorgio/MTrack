import logging
from datetime import date, datetime
from uuid import UUID
from src.clients.postgres_client import PostgresClient
from src.repositories import queries as q
from src.models.transactions import Transaction

logger = logging.getLogger(__name__)

class TransactionsRepository:
    def __init__(self, postgres_client: PostgresClient):
        self.__postgres_client = postgres_client

    async def get_transactions(self, start_date: datetime, end_date: datetime) -> list[Transaction] | None:
        logger.debug("Executing transactions query...")
        transactions = None
        async with self.__postgres_client.async_session() as session:
            try:
                result = await session.execute(q.GET_TRANSACTIONS, {
                    "start_date": start_date,
                    "end_date": end_date,
                })
                rows = result.mappings().all()
                transactions = [ Transaction(**row) for row in rows ]
                logger.debug(f"Transactions data retrieved!")
            except Exception as e:
                logger.error(f"Error fetching transactions data", exc_info=e)
        return transactions
    
    async def update_transaction(
        self,
        transaction_id: UUID,
        primary_category_id: UUID | None = None,
        secondary_category_id: UUID | None = None,
        amount: float | None = None,
        transaction_date: date | None = None,
        update_primary: bool = False,
        update_secondary: bool = False,
        update_amount: bool = False,
        update_date: bool = False,
    ) -> Transaction | None:
        logger.debug(f"Executing update transaction query for transaction {transaction_id}...")
        updated_transaction = None
        async with self.__postgres_client.async_session() as session:
            try:
                result = await session.execute(q.UPDATE_TRANSACTION, {
                    "transaction_id": str(transaction_id),
                    "amount": amount,
                    "transaction_date": transaction_date,
                    "primary_category_id": str(primary_category_id) if primary_category_id else None,
                    "secondary_category_id": str(secondary_category_id) if secondary_category_id else None,
                    "update_amount": update_amount,
                    "update_date": update_date,
                    "update_primary": update_primary,
                    "update_secondary": update_secondary,
                })
                row = result.mappings().first()
                if row:
                    updated_transaction = Transaction(**row)
                    logger.debug(f"Transaction {transaction_id} updated successfully!")
                else:
                    logger.warning(f"Transaction {transaction_id} not found for update.")
                await session.commit()
            except Exception as e:
                logger.error(f"Error updating transaction {transaction_id}", exc_info=e)
                await session.rollback()
        return updated_transaction

    async def delete_transaction(self, transaction_id: UUID) -> bool:
        logger.debug(f"Executing delete transaction query for transaction {transaction_id}...")
        deleted = False
        async with self.__postgres_client.async_session() as session:
            try:
                result = await session.execute(q.DELETE_TRANSACTION, {
                    "transaction_id": str(transaction_id)
                })
                deleted = result.first() is not None
                await session.commit()
                if deleted:
                    logger.debug(f"Transaction {transaction_id} deleted successfully!")
                else:
                    logger.warning(f"Transaction {transaction_id} not found for deletion.")
            except Exception as e:
                logger.error(f"Error deleting transaction {transaction_id}", exc_info=e)
                await session.rollback()
        return deleted