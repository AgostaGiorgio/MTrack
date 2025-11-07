from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, Float, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.db.models.base import Base

if TYPE_CHECKING:
    from src.db.models.card_account import CardAccount
    from src.db.models.category import Category


class Expense(Base):
    __tablename__ = "expenses"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    card_account: Mapped[str] = mapped_column(
        String(50), 
        ForeignKey("card_accounts.card_number", ondelete="RESTRICT")
    )
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    reimbursed: Mapped[float] = mapped_column(Float, default=0.0)
    description: Mapped[str] = mapped_column(String(500))
    primary_category: Mapped[str] = mapped_column(
        String(100), 
        ForeignKey("categories.name", ondelete="RESTRICT")
    )
    secondary_category: Mapped[Optional[str]] = mapped_column(
        String(100), 
        ForeignKey("categories.name", ondelete="SET NULL")
    )
    
    # Relationships
    card: Mapped["CardAccount"] = relationship(back_populates="expenses")
    primary_cat: Mapped["Category"] = relationship(
        back_populates="expenses_as_primary",
        foreign_keys=[primary_category]
    )
    secondary_cat: Mapped[Optional["Category"]] = relationship(
        back_populates="expenses_as_secondary",
        foreign_keys=[secondary_category]
    )
    
    def __repr__(self):
        return f"🗓️ {self.timestamp.isoformat(sep=' ')} 💳 {self.amount} 📜 {self.description}"
    
    def to_dict(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat(),
            "card_account": self.card_account,
            "amount": self.amount,
            "description": self.description,
            "primary_category": self.primary_category,
            "secondary_category": self.secondary_category if self.secondary_category else "",
            "reimbursed": self.reimbursed
        }
        
    @classmethod
    def from_json(cls, data: dict) -> "Expense":
        ts = data.get("timestamp")
        if isinstance(ts, str):
            data = data.copy()
            data["timestamp"] = datetime.fromisoformat(ts)
        return cls(**data)