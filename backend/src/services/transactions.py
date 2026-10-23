import logging
from datetime import date
from uuid import UUID
import copy
from src.repositories.transactions import TransactionsRepository
from src.repositories.categories import CategoriesRepository
from src.models.transactions import Transaction
from src.models.categories import Category
from src.utils.date_utils import get_mtrack_month_range

logger = logging.getLogger(__name__)

class TransactionsService:
    def __init__(self, 
                 transactions_repository: TransactionsRepository,
                 categories_repository: CategoriesRepository):
        self.__transactions_repository = transactions_repository
        self.__categories_repository = categories_repository

    async def get_transactions(self, year: int | None = None, month: int | None = None) -> list[Transaction]:
        logger.info("Fetching transactions...")
        start_date, end_date = get_mtrack_month_range(year, month)
        transactions = await self.__transactions_repository.get_transactions(start_date, end_date)
        categories = await self.__categories_repository.get_categories()
        
        for transaction in transactions:
            transaction = self.__replace_categories(transaction, categories)
                
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
        logger.info(f"Updating transaction {transaction_id}...")
        updated_transaction = await self.__transactions_repository.update_transaction(
            transaction_id=transaction_id,
            primary_category_id=primary_category_id,
            secondary_category_id=secondary_category_id,
            amount=amount,
            transaction_date=transaction_date,
            update_primary=update_primary,
            update_secondary=update_secondary,
            update_amount=update_amount,
            update_date=update_date,
        )
        if updated_transaction is None:
            logger.warning(f"Transaction {transaction_id} not found.")
            return None
        logger.info(f"Transaction {transaction_id} updated successfully!")
        categories = await self.__categories_repository.get_categories()
        return self.__replace_categories(updated_transaction, categories)

    async def delete_transaction(self, transaction_id: UUID) -> bool:
        logger.info(f"Deleting transaction {transaction_id}...")
        return await self.__transactions_repository.delete_transaction(transaction_id)

    def __replace_categories(self, transaction: Transaction, categories: list[Category]) -> Transaction:
        if transaction.primary_category and isinstance(transaction.primary_category, UUID):
            primary = next((c for c in categories if str(c.id) == str(transaction.primary_category)), None)
            transaction.primary_category = copy.copy(primary) if primary else None

        if transaction.secondary_category and isinstance(transaction.secondary_category, UUID):
            subcategories = [sub for category in categories for sub in (category.sub_categories or [])]
            secondary = next((c for c in subcategories if str(c.id) == str(transaction.secondary_category)), None)
            transaction.secondary_category = copy.copy(secondary) if secondary else None

        if isinstance(transaction.primary_category, Category):
            transaction.primary_category.sub_categories = None
        if isinstance(transaction.secondary_category, Category):
            transaction.secondary_category.sub_categories = None
        return transaction