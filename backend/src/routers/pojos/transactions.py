from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import date as ddate

class UpdateTransaction(BaseModel):
    amount: Optional[float] = Field(None, ge=0, description="Updated amount of the transaction")
    date: Optional[ddate] = Field(None, description="Updated date (YYYY-MM-DD) of the transaction")
    primary_category_id: Optional[UUID] = Field(None, description="ID of the primary category")
    secondary_category_id: Optional[UUID] = Field(None, description="ID of the secondary category")
