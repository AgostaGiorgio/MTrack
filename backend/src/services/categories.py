import logging
from uuid import UUID
from src.repositories.categories import CategoriesRepository
from src.models.categories import Category

logger = logging.getLogger(__name__)

class CategoriesService:
    def __init__(self, categories_repository: CategoriesRepository):
        self.__categories_repository = categories_repository

    async def get_categories(self) -> list[Category] | None:
        logger.info("Fetching categories data...")
        return await self.__categories_repository.get_categories()
    
    async def create_category(self, name: str, icon: str, primary_id: UUID | None) -> Category:
        logger.info(f"Creating category with name: {name} and icon: {icon}")
        return await self.__categories_repository.create_category(name=name, icon=icon, primary_id=primary_id)
    
    async def update_category(self, category_id: UUID, name: str, icon: str) -> Category:
        logger.info(f"Updating category with id: {category_id} to have name: {name} and icon: {icon}")
        return await self.__categories_repository.update_category(category_id=category_id, name=name, icon=icon)
    
    async def unlink_sub_category(self, category_id: UUID, sub_category_id: UUID):
        logger.info(f"Unlinking sub-category {sub_category_id} from category {category_id}")
        await self.__categories_repository.unlink_sub_category(category_id=category_id, sub_category_id=sub_category_id)