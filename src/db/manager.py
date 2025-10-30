from src.config.logger import *
from src.config.config import settings

from typing import Optional, List, Dict, Any
from datetime import datetime
from sqlalchemy import select, func, delete, text, and_
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError
import asyncpg

from src.db.models.base import Base
from src.db.models.expense import Expense
from src.db.models.card_account import CardAccount
from src.db.models.category import Category 
from src.db.models.primary_secondary_category import PrimarySecondaryCategory

logger = logging.getLogger(__name__)

class MTrackDB:
    def __init__(self):
        self.connection_url = f"postgresql+asyncpg://{settings.postgres_user}:{settings.postgres_password}@{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_database}"
        self.base_url = f"postgresql://{settings.postgres_user}:{settings.postgres_password}@{settings.postgres_host}:{settings.postgres_port}"
        
        self.engine = None
        self.async_session = None
    
    async def initialize(self):
        """Initialize database connection and create tables"""
        await self.__ensure_database_exists()
        
        self.engine = create_async_engine(self.connection_url, echo=False)
        self.async_session = async_sessionmaker(
            self.engine, 
            class_=AsyncSession, 
            expire_on_commit=False
        )
        # Create all tables
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            
        if settings.mtrack_categories:
            logger.debug("Pre-populating categories...")
            for name in settings.mtrack_categories:
                await self.add_category(name=name, ignore_if_exists=True)
            logger.debug("Categories pre-populated successfully")
        if settings.mtrack_primary_secondary_categories:
            logger.debug("Pre-populating primary-secondary category mappings...")
            for primary, secondary in settings.mtrack_primary_secondary_categories:
                await self.add_primary_secondary_mapping(primary=primary, secondary=secondary, ignore_if_exists=True)
            logger.debug("Primary-secondary category mappings pre-populated successfully")
        if settings.mtrack_card_accounts:
            logger.debug("Pre-populating card accounts...")
            for card_number in settings.mtrack_card_accounts:
                await self.add_card_account(card_number=card_number, ignore_if_exists=True)
            logger.debug("Card accounts pre-populated successfully")
        
        logger.debug("Database initialized successfully")

    
    async def __ensure_database_exists(self):
        """Create database if it doesn't exist"""
        try:
            # Connect to postgres database to create our database
            conn = await asyncpg.connect(self.base_url + "/postgres")
            
            # Check if database exists
            exists = await conn.fetchval(
                "SELECT 1 FROM pg_database WHERE datname = $1", settings.postgres_database
            )
            
            if not exists:
                # Cannot create database inside a transaction
                await conn.execute(f'CREATE DATABASE {settings.postgres_database}')
                logger.info(f"Database '{settings.postgres_database}' created successfully")
            else:
                logger.info(f"Database '{settings.postgres_database}' already exists")
            
            await conn.close()
        except Exception as e:
            logger.error(f"Error ensuring database exists: {e}")
            raise
    
    async def close(self):
        """Close database connection"""
        if self.engine:
            await self.engine.dispose()
    
    # ========== Card Account Methods ==========
    
    async def add_card_account(self, card_number: str, ignore_if_exists: bool = False) -> CardAccount:
        """Add a new card account"""
        async with self.async_session() as session:
            card = CardAccount(card_number=card_number)
            session.add(card)
            try:
                await session.commit()
                await session.refresh(card)
            except IntegrityError as e:
                if ignore_if_exists:
                    logger.debug(f"Card account '{card_number}' already exists, ignoring as per flag.")
                else:
                    raise e
            return card
    
    async def get_or_create_card_account(self, card_number: str) -> CardAccount:
        """Get existing card account or create if doesn't exist"""
        async with self.async_session() as session:
            result = await session.execute(
                select(CardAccount).where(CardAccount.card_number == card_number)
            )
            card = result.scalar_one_or_none()
            
            if not card:
                card = CardAccount(card_number=card_number)
                session.add(card)
                await session.commit()
                await session.refresh(card)
            
            return card
    
    async def get_all_card_accounts(self) -> List[CardAccount]:
        """Get all card accounts"""
        async with self.async_session() as session:
            result = await session.execute(select(CardAccount))
            return result.scalars().all()
    
    async def delete_card_account(self, card_number: str) -> bool:
        """Delete a card account (only if no expenses reference it)"""
        async with self.async_session() as session:
            result = await session.execute(
                delete(CardAccount).where(CardAccount.card_number == card_number)
            )
            await session.commit()
            return result.rowcount > 0
    
    # ========== Category Methods ==========
    
    async def add_category(self, name: str, ignore_if_exists: bool = False) -> Category:
        """Add a new category"""
        async with self.async_session() as session:
            category = Category(name=name)
            session.add(category)
            try:
                await session.commit()
                await session.refresh(category)
            except IntegrityError as e:
                if ignore_if_exists:
                    logger.debug(f"Category '{name}' already exists, ignoring as per flag.")
                else:
                    raise e
                
            return category
    
    async def get_all_categories(self) -> List[Category]:
        """Get all categories"""
        async with self.async_session() as session:
            result = await session.execute(select(Category))
            return result.scalars().all()
    
    async def delete_category(self, name: str) -> bool:
        """Delete a category (only if no expenses reference it)"""
        async with self.async_session() as session:
            result = await session.execute(
                delete(Category).where(Category.name == name)
            )
            await session.commit()
            return result.rowcount > 0
    
    # ========== Primary-Secondary Category Mapping Methods ==========
    
    async def add_primary_secondary_mapping(self, primary: str, secondary: str, ignore_if_exists: bool = False) -> PrimarySecondaryCategory:
        """Add a mapping between primary and secondary category"""
        async with self.async_session() as session:
            mapping = PrimarySecondaryCategory(
                primary_category=primary,
                secondary_category=secondary
            )
            session.add(mapping)
            try:
                await session.commit()
                await session.refresh(mapping)
            except IntegrityError as e:
                if ignore_if_exists:
                    logger.debug(f"Relation between {primary} and {secondary} already exists, ignoring as per flag.", exc_info=e)
                else:
                    raise e
            return mapping
    
    async def get_secondary_categories_for_primary(self, primary: str) -> List[str]:
        """Get all secondary categories for a given primary category"""
        async with self.async_session() as session:
            result = await session.execute(
                select(PrimarySecondaryCategory.secondary_category)
                .where(PrimarySecondaryCategory.primary_category == primary)
            )
            return [row[0] for row in result]
    
    async def get_all_primary_secondary_mappings(self) -> Dict[str, List[str]]:
        """Get all primary-secondary mappings as a dictionary"""
        async with self.async_session() as session:
            result = await session.execute(
                select(PrimarySecondaryCategory)
                .options(
                    selectinload(PrimarySecondaryCategory.primary),
                    selectinload(PrimarySecondaryCategory.secondary)
                )
            )
            mappings = result.scalars().all()
            
            # Group by primary category
            grouped: Dict[str, List[str]] = {}
            for mapping in mappings:
                if mapping.primary_category not in grouped:
                    grouped[mapping.primary_category] = []
                grouped[mapping.primary_category].append(mapping.secondary_category)
            
            return grouped
    
    async def delete_primary_secondary_mapping(self, primary: str, secondary: str) -> bool:
        """Delete a primary-secondary mapping"""
        async with self.async_session() as session:
            result = await session.execute(
                delete(PrimarySecondaryCategory).where(
                    and_(
                        PrimarySecondaryCategory.primary_category == primary,
                        PrimarySecondaryCategory.secondary_category == secondary
                    )
                )
            )
            await session.commit()
            return result.rowcount > 0
    
    async def is_valid_secondary_for_primary(self, primary: str, secondary: str) -> bool:
        """Check if a secondary category is valid for a given primary category"""
        async with self.async_session() as session:
            result = await session.execute(
                select(PrimarySecondaryCategory).where(
                    and_(
                        PrimarySecondaryCategory.primary_category == primary,
                        PrimarySecondaryCategory.secondary_category == secondary
                    )
                )
            )
            return result.scalar_one_or_none() is not None
    
    # ========== Expense Methods ==========
    
    async def add_expense(self, expense_data: Dict[str, Any]) -> Expense:
        """Add a new expense"""
        async with self.async_session() as session:
            # Ensure card account exists
            await self.get_or_create_card_account(expense_data["card_account"])
            
            # Check that primary category exists
            result = await session.execute(
                select(Category).where(Category.name == expense_data["primary_category"])
            )
            if not result.scalar_one_or_none():
                raise ValueError(f"Primary category '{expense_data['primary_category']}' does not exist")
            
            # Check secondary category if provided
            secondary = expense_data.get("secondary_category")
            if secondary:
                # Check that secondary category exists
                result = await session.execute(
                    select(Category).where(Category.name == secondary)
                )
                if not result.scalar_one_or_none():
                    raise ValueError(f"Secondary category '{secondary}' does not exist")
                
                # Check that the mapping exists
                if not await self.is_valid_secondary_for_primary(expense_data["primary_category"], secondary):
                    raise ValueError(
                        f"Secondary category '{secondary}' is not valid for "
                        f"primary category '{expense_data['primary_category']}'"
                    )
            
            # Parse timestamp
            timestamp = datetime.fromisoformat(expense_data["timestamp"])
            
            # Create expense
            expense = Expense(
                timestamp=timestamp,
                card_account=expense_data["card_account"],
                amount=expense_data["amount"],
                description=expense_data.get("description", ""),
                primary_category=expense_data["primary_category"],
                secondary_category=secondary if secondary else None,
                reimbursed=expense_data.get("reimbursed", 0.0)
            )
            
            session.add(expense)
            await session.commit()
            await session.refresh(expense)
            
            # Load relationships
            await session.refresh(expense, ["card", "primary_cat", "secondary_cat"])
            return expense
    
    async def update_expense(self, expense_id: int, expense_data: Dict[str, Any]) -> Expense:
        """Update an existing expense"""
        async with self.async_session() as session:
            result = await session.execute(
                select(Expense).where(Expense.id == expense_id)
            )
            expense = result.scalar_one_or_none()
            
            if not expense:
                raise ValueError(f"Expense with id {expense_id} not found")
            
            # Update fields if provided
            if "timestamp" in expense_data:
                expense.timestamp = datetime.fromisoformat(expense_data["timestamp"])
            
            if "card_account" in expense_data:
                await self.get_or_create_card_account(expense_data["card_account"])
                expense.card_account = expense_data["card_account"]
            
            if "amount" in expense_data:
                expense.amount = expense_data["amount"]
            
            if "description" in expense_data:
                expense.description = expense_data["description"]
            
            if "primary_category" in expense_data:
                result = await session.execute(
                    select(Category).where(Category.name == expense_data["primary_category"])
                )
                if not result.scalar_one_or_none():
                    raise ValueError(f"Primary category '{expense_data['primary_category']}' does not exist")
                expense.primary_category = expense_data["primary_category"]
            
            if "secondary_category" in expense_data:
                secondary = expense_data["secondary_category"]
                if secondary:
                    result = await session.execute(
                        select(Category).where(Category.name == secondary)
                    )
                    if not result.scalar_one_or_none():
                        raise ValueError(f"Secondary category '{secondary}' does not exist")
                    
                    # Use the current primary_category (which might have been just updated)
                    primary = expense_data.get("primary_category", expense.primary_category)
                    if not await self.is_valid_secondary_for_primary(primary, secondary):
                        raise ValueError(
                            f"Secondary category '{secondary}' is not valid for "
                            f"primary category '{primary}'"
                        )
                    expense.secondary_category = secondary
                else:
                    expense.secondary_category = None
            
            if "reimbursed" in expense_data:
                expense.reimbursed = expense_data["reimbursed"]
            
            await session.commit()
            await session.refresh(expense, ["card", "primary_cat", "secondary_cat"])
            return expense
    
    async def delete_expense(self, expense_id: int) -> bool:
        """Delete an expense"""
        async with self.async_session() as session:
            result = await session.execute(
                delete(Expense).where(Expense.id == expense_id)
            )
            await session.commit()
            return result.rowcount > 0
    
    async def get_expense(self, expense_id: int) -> Optional[Expense]:
        """Get a single expense by ID"""
        async with self.async_session() as session:
            result = await session.execute(
                select(Expense)
                .options(
                    selectinload(Expense.card),
                    selectinload(Expense.primary_cat),
                    selectinload(Expense.secondary_cat)
                )
                .where(Expense.id == expense_id)
            )
            return result.scalar_one_or_none()
    
    async def get_all_expenses(self) -> List[Expense]:
        """Get all expenses"""
        async with self.async_session() as session:
            result = await session.execute(
                select(Expense)
                .options(
                    selectinload(Expense.card),
                    selectinload(Expense.primary_cat),
                    selectinload(Expense.secondary_cat)
                )
                .order_by(Expense.timestamp.desc())
            )
            return result.scalars().all()
    
    async def get_expenses_by_primary_category(self, category_name: str) -> List[Expense]:
        """Get all expenses for a primary category"""
        async with self.async_session() as session:
            result = await session.execute(
                select(Expense)
                .options(
                    selectinload(Expense.card),
                    selectinload(Expense.primary_cat),
                    selectinload(Expense.secondary_cat)
                )
                .where(Expense.primary_category == category_name)
                .order_by(Expense.timestamp.desc())
            )
            return result.scalars().all()
    
    async def get_expenses_by_secondary_category(self, category_name: str) -> List[Expense]:
        """Get all expenses for a secondary category"""
        async with self.async_session() as session:
            result = await session.execute(
                select(Expense)
                .options(
                    selectinload(Expense.card),
                    selectinload(Expense.primary_cat),
                    selectinload(Expense.secondary_cat)
                )
                .where(Expense.secondary_category == category_name)
                .order_by(Expense.timestamp.desc())
            )
            return result.scalars().all()
    
    async def get_expenses_by_card(self, card_number: str) -> List[Expense]:
        """Get all expenses for a card account"""
        async with self.async_session() as session:
            result = await session.execute(
                select(Expense)
                .options(
                    selectinload(Expense.card),
                    selectinload(Expense.primary_cat),
                    selectinload(Expense.secondary_cat)
                )
                .where(Expense.card_account == card_number)
                .order_by(Expense.timestamp.desc())
            )
            return result.scalars().all()
    
    async def get_category_summary(self) -> List[Dict[str, Any]]:
        """Get total spending grouped by primary category"""
        async with self.async_session() as session:
            result = await session.execute(
                select(
                    Expense.primary_category,
                    func.sum(Expense.amount).label("total"),
                    func.count(Expense.id).label("count")
                )
                .group_by(Expense.primary_category)
                .order_by(func.sum(Expense.amount).desc())
            )
            
            return [
                {"category": row.primary_category, "total": float(row.total), "count": row.count}
                for row in result
            ]
    
    async def get_secondary_category_summary(self) -> List[Dict[str, Any]]:
        """Get total spending grouped by secondary category"""
        async with self.async_session() as session:
            result = await session.execute(
                select(
                    Expense.secondary_category,
                    func.sum(Expense.amount).label("total"),
                    func.count(Expense.id).label("count")
                )
                .where(Expense.secondary_category.is_not(None))
                .group_by(Expense.secondary_category)
                .order_by(func.sum(Expense.amount).desc())
            )
            
            return [
                {"category": row.secondary_category, "total": float(row.total), "count": row.count}
                for row in result
            ]
    
    async def get_card_summary(self) -> List[Dict[str, Any]]:
        """Get total spending grouped by card account"""
        async with self.async_session() as session:
            result = await session.execute(
                select(
                    Expense.card_account,
                    func.sum(Expense.amount).label("total"),
                    func.count(Expense.id).label("count")
                )
                .group_by(Expense.card_account)
                .order_by(func.sum(Expense.amount).desc())
            )
            
            return [
                {"card": row.card_account, "total": float(row.total), "count": row.count}
                for row in result
            ]
    
    # ========== Raw Query Method ==========
    
    async def execute_raw_query(self, query: str, params: Optional[Dict] = None):
        """Execute a raw SQL query"""
        async with self.async_session() as session:
            result = await session.execute(text(query), params or {})
            await session.commit()
            return result