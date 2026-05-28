from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID

class CardSummary(BaseModel):
    name: str = Field(..., description="Name of the card")
    amount: float = Field(..., description="Amount spent on this card")
    
class CategorySummary(BaseModel):
    id: UUID = Field(..., description="Unique identifier of the category")
    name: str = Field(..., description="Name of the category")
    amount: float = Field(..., description="Amount spent in this category")
    sub_categories: Optional[list['CategorySummary']] = Field(default_factory=list, description="Subcategories of this category")
    
class MonthlyTrend(BaseModel):
    month: str = Field(..., description="Month")
    amount: float = Field(..., description="Amount spent in this month")

class DashboardData(BaseModel):
    current_month: str = Field(..., description="Current month in format 'YYYY MM'")
    total_spent: float = Field(..., description="Total amount spent in the current month")
    cards_summary: list[CardSummary] = Field(default_factory=list, description="Summary of each card's spending")
    categories_summary: list[CategorySummary] = Field(default_factory=list, description="Summary of spending by category")
    monthly_trends: list[MonthlyTrend] = Field(default_factory=list, description="Trends of spending over the last year month by month")