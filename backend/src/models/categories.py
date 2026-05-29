from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID

class Category(BaseModel):
    id: UUID = Field(..., description="Unique identifier of the category")
    name: str = Field(..., description="Name of the category")
    icon: Optional[str] = Field(None, description="Icon associated with the category")
    sub_categories: Optional[list['Category']] = Field(default_factory=list, description="Subcategories of this category")