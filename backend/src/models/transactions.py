from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime

from src.models.categories import Category

class Transaction(BaseModel):
    id: UUID = Field(..., description="Unique identifier of the transaction")
    amount: float = Field(..., description="Amount of the transaction")
    date: datetime = Field(..., description="Date of the transaction in format 'YYYY-MM-DD'")
    description: Optional[str] = Field(None, description="Description of the transaction")
    card: str = Field(None, description="Card associated with the transaction")
    primary_category: Optional[Category] | Optional[UUID] = Field(None, description="Category associated with the transaction")
    secondary_category: Optional[Category] | Optional[UUID] = Field(None, description="Secondary category associated with the transaction")