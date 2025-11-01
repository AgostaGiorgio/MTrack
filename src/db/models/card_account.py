from typing import List, TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.db.models.base import Base

if TYPE_CHECKING:
    from src.db.models.expense import Expense


class CardAccount(Base):
    __tablename__ = "card_accounts"
    
    card_number: Mapped[str] = mapped_column(String(50), primary_key=True)
    
    # Relationship
    expenses: Mapped[List["Expense"]] = relationship(back_populates="card")
    
    def __repr__(self) -> str:
        return f"<CardAccount(card_number='{self.card_number}')>"
    
    def to_msg(self) -> str:
        return f"• {self.card_number}"