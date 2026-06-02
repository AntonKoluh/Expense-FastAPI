from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import mapped_column, relationship, Mapped
from db.base import Base
from .associations import transaction_category_association



class Transactions(Base):
    __tablename__ = "transaction"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    amount: Mapped[int] = mapped_column(Integer(), nullable=True)
    categories: Mapped[list["Categories"]] = relationship(
        secondary = transaction_category_association,
        back_populates="transactions"
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))