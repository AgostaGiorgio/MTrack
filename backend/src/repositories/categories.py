import logging
from uuid import UUID
from src.clients.postgres_client import PostgresClient
from src.repositories import queries as q
from src.models.categories import Category

logger = logging.getLogger(__name__)

class CategoriesRepository:
    def __init__(self, postgres_client: PostgresClient):
        self.__postgres_client = postgres_client

    async def get_categories(self) -> list[Category] | None:
        logger.debug("Executing categories query...")
        categories = None
        async with self.__postgres_client.async_session() as session:
            try:
                result = await session.execute(q.GET_CATEGORIES)
                rows = result.mappings().all()
                categories = { row['id']: Category(**row) for row in rows }
                logger.debug(f"Categories data retrieved!")
            except Exception as e:
                logger.error(f"Error fetching categories data", exc_info=e)
                
            try:
                result = await session.execute(q.GET_CATEGORIES_MAPPING)
                rows = result.mappings().all()
                for row in rows:
                    category = categories.get(row['id'])
                    if category:
                        category.sub_categories = [ Category(**sub_row) for sub_row in row['secondary_categories'] ]
            except Exception as e:
                logger.error(f"Error fetching sub categories data", exc_info=e)
        return categories.values() if categories else None
    
    async def create_category(self, name: str, icon: str, primary_id: UUID | None) -> Category | None:
        logger.debug(f"Executing create category query with name: {name} and icon: {icon}...")
        category = None
        
        type = 'primary'
        if primary_id:
            type = 'secondary'
        
        async with self.__postgres_client.async_session() as session:
            try:
                result = await session.execute(q.CREATE_CATEGORY, {"name": name, "icon": icon, "type": type})
                row = result.mappings().first()
                if row:
                    category = Category(**row)
                logger.debug(f"Category created with id: {category.id}")
                
                if primary_id:
                    await session.execute(q.CREATE_CATEGORY_MAPPING, {"primary_id": str(primary_id), "secondary_id": str(category.id)})
                await session.commit()
            except Exception as e:
                logger.error(f"Error creating category", exc_info=e)
                await session.rollback()
        return category
    
    async def update_category(self, category_id: UUID, name: str, icon: str) -> Category | None:
        logger.debug(f"Executing update category query for category id: {category_id} with name: {name} and icon: {icon}...")
        category = None
        async with self.__postgres_client.async_session() as session:
            try:
                result = await session.execute(q.UPDATE_CATEGORY, {"id": str(category_id), "name": name, "icon": icon})
                row = result.mappings().first()
                if row:
                    category = Category(**row)
                logger.debug(f"Category updated with id: {category.id}")
                await session.commit()
            except Exception as e:
                logger.error(f"Error updating category", exc_info=e)
                await session.rollback()
        return category