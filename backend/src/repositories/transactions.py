import logging
from datetime import datetime
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
    
    async def update_transaction_categories(self, transaction_id: UUID, primary_category_id: UUID, secondary_category_id: UUID | None) -> Transaction:
        logger.debug(f"Executing update transaction categories query for transaction {transaction_id}...")
        updated_transaction = None
        async with self.__postgres_client.async_session() as session:
            try:
                result = await session.execute(q.UPDATE_TRANSACTION_CATEGORIES, {
                    "transaction_id": str(transaction_id),
                    "primary_category_id": str(primary_category_id),
                    "secondary_category_id": str(secondary_category_id) if secondary_category_id else None
                })
                row = result.mappings().first()
                if row:
                    updated_transaction = Transaction(**row)
                    logger.debug(f"Transaction {transaction_id} categories updated successfully!")
                else:
                    logger.warning(f"Transaction {transaction_id} not found for category update.")
                await session.commit()
            except Exception as e:
                logger.error(f"Error updating categories for transaction {transaction_id}", exc_info=e)
                await session.rollback()
        return updated_transaction