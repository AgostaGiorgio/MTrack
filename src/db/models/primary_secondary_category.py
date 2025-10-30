from typing import TYPE_CHECKING
from sqlalchemy import String, ForeignKey, UniqueConstraint, CheckConstraint, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.db.models.base import Base

if TYPE_CHECKING:
    from src.db.models.category import Category


class PrimarySecondaryCategory(Base):
    __tablename__ = "primary_secondary_cat"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    primary_category: Mapped[str] = mapped_column(
        String(100), 
        ForeignKey("categories.name", ondelete="CASCADE")
    )
    secondary_category: Mapped[str] = mapped_column(
        String(100), 
        ForeignKey("categories.name", ondelete="CASCADE")
    )
    
    # Relationships
    primary: Mapped["Category"] = relationship(
        back_populates="primary_mappings",
        foreign_keys=[primary_category]
    )
    secondary: Mapped["Category"] = relationship(
        back_populates="secondary_mappings",
        foreign_keys=[secondary_category]
    )
    
    # Constraints
    __table_args__ = (
        UniqueConstraint('primary_category', 'secondary_category', name='uq_primary_secondary'),
        CheckConstraint('primary_category != secondary_category', name='check_different_categories'),
    )
    
    def __repr__(self):
        return f"<PrimarySecondaryCategory(primary='{self.primary_category}', secondary='{self.secondary_category}')>"
