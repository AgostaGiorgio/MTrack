from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import date as ddate, time as ttime

class CreateTransaction(BaseModel):
    amount: float = Field(..., gt=0, description="Amount of the transaction")
    date: ddate = Field(..., description="Date (YYYY-MM-DD) of the transaction")
    time: Optional[ttime] = Field(None, description="Time (HH:MM:SS) of the transaction")
    description: Optional[str] = Field(None, description="Description of the transaction")
    card: Optional[str] = Field('Manual', description="Card associated with the transaction")
    card_limit: Optional[float] = Field(0, ge=0, description="Card limit associated with the transaction")
    primary_category_id: Optional[UUID] = Field(None, description="ID of the primary category")
    secondary_category_id: Optional[UUID] = Field(None, description="ID of the secondary category")

class UpdateTransaction(BaseModel):
    amount: Optional[float] = Field(None, ge=0, description="Updated amount of the transaction")
    date: Optional[ddate] = Field(None, description="Updated date (YYYY-MM-DD) of the transaction")
    primary_category_id: Optional[UUID] = Field(None, description="ID of the primary category")
    secondary_category_id: Optional[UUID] = Field(None, description="ID of the secondary category")
