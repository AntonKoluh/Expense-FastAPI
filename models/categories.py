from sqlalchemy import ForeignKey
from sqlalchemy import String, Integer
from db.base import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, relationship
from .transactions import transaction_category_association

class Categories(Base):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    limit: Mapped[int] = mapped_column(Integer(), nullable=True)
    transactions: Mapped[list["Transactions"]] = relationship(
        secondary = transaction_category_association,
        back_populates="categories"
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))