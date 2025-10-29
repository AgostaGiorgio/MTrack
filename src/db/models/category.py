from typing import List, TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.db.models.base import Base

if TYPE_CHECKING:
    from src.db.models.expense import Expense
    from src.db.models.primary_secondary_category import PrimarySecondaryCategory


class Category(Base):
    __tablename__ = "categories"
    
    name: Mapped[str] = mapped_column(String(100), primary_key=True)
    
    # Relationships
    expenses_as_primary: Mapped[List["Expense"]] = relationship(
        back_populates="primary_cat",
        foreign_keys="[Expense.primary_category]"
    )
    expenses_as_secondary: Mapped[List["Expense"]] = relationship(
        back_populates="secondary_cat",
        foreign_keys="[Expense.secondary_category]"
    )
    primary_mappings: Mapped[List["PrimarySecondaryCategory"]] = relationship(
        back_populates="primary",
        foreign_keys="[PrimarySecondaryCategory.primary_category]"
    )
    secondary_mappings: Mapped[List["PrimarySecondaryCategory"]] = relationship(
        back_populates="secondary",
        foreign_keys="[PrimarySecondaryCategory.secondary_category]"
    )
    
    def __repr__(self):
        return f"<Category(name='{self.name}')>"