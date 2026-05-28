from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID

class NewCategory(BaseModel):
    name: str = Field(..., description="Name of the category")
    icon: Optional[str] = Field(None, description="Icon associated with the category")
    parentId: Optional[UUID] = Field(None, description="ID of the parent category, if this is a sub-category")