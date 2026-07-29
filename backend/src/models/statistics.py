from pydantic import BaseModel, Field
from src.models.dashboard import MonthlyTrend


class CategoryMonthlyTrend(BaseModel):
    category_name: str = Field(..., description="Name of the category")
    monthly_data: list[MonthlyTrend] = Field(
        default_factory=list, description="Monthly spending data for this category"
    )


class StatisticsData(BaseModel):
    monthly_trends: list[MonthlyTrend] = Field(
        default_factory=list, description="Monthly spending totals for the year"
    )
    category_trends: list[CategoryMonthlyTrend] = Field(
        default_factory=list,
        description="Monthly spending per tracked category",
    )
    current_month: str = Field(..., description="Current month label")
    total_spent: float = Field(0.0, description="Total spending for current month")
