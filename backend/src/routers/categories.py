from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide
from uuid import UUID
from src.di import Container

from src.models.categories import Category
from src.routers.pojos.categories import NewCategory
from src.services.categories import CategoriesService


api_router = APIRouter()

@api_router.get("", response_model=list[Category], status_code=200)
@inject
async def get_categories(categories_service: CategoriesService = Depends(Provide[Container.categories_service])) -> list[Category]:
    return await categories_service.get_categories()

@api_router.post("", response_model=Category, status_code=201)
@inject
async def create_category(new_category: NewCategory, categories_service: CategoriesService = Depends(Provide[Container.categories_service])) -> Category:
    return await categories_service.create_category(name=new_category.name, icon=new_category.icon, primary_id=new_category.parentId)

@api_router.put("/{category_id}", response_model=Category, status_code=200)
@inject
async def update_category(category_id: UUID, category_data: NewCategory, categories_service: CategoriesService = Depends(Provide[Container.categories_service])) -> Category:
    return await categories_service.update_category(category_id=category_id, name=category_data.name, icon=category_data.icon)

@api_router.put("/{category_id}/sub/{sub_category_id}/unlink", status_code=204)
@inject
async def unlink_sub_category(category_id: UUID, sub_category_id: UUID, categories_service: CategoriesService = Depends(Provide[Container.categories_service])):
    await categories_service.unlink_sub_category(category_id=category_id, sub_category_id=sub_category_id)