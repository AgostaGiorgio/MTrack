import logging
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
    
    async def update_transaction_categories(self, transaction_id: UUID, primary_category_id: UUID, secondary_category_id: UUID | None) -> Transaction:
        logger.info(f"Updating categories for transaction {transaction_id}...")
        updated_transaction = await self.__transactions_repository.update_transaction_categories(
            transaction_id=transaction_id,
            primary_category_id=primary_category_id,
            secondary_category_id=secondary_category_id
        )
        logger.info(f"Transaction {transaction_id} categories updated successfully!")
        categories = await self.__categories_repository.get_categories()
        updated_transaction = self.__replace_categories(updated_transaction, categories)
        return updated_transaction
        
    def __replace_categories(self, transaction: Transaction, categories: list[Category]) -> Transaction:
        if transaction.primary_category and isinstance(transaction.primary_category, UUID):
            category = next((c for c in categories if str(c.id) == str(transaction.primary_category)), None)
            transaction.primary_category = copy.copy(category)
        if transaction.secondary_category and isinstance(transaction.secondary_category, UUID):
            category = next((c for c in category.sub_categories if str(c.id) == str(transaction.secondary_category)), None)
            transaction.secondary_category = copy.copy(category)
        if isinstance(transaction.primary_category, Category):
            transaction.primary_category.sub_categories = None
        if isinstance(transaction.secondary_category, Category):
            transaction.secondary_category.sub_categories = None
        return transaction