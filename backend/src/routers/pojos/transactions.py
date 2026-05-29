from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID

class UpdateTransactionCategories(BaseModel):
    primary_category_id: UUID = Field(..., description="ID of the primary category")
    secondary_category_id: Optional[UUID] = Field(None, description="ID of the secondary category")