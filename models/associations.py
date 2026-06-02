from sqlalchemy import ForeignKey, Table, Column
from db.base import Base

transaction_category_association = Table(
    "transaction_category",
    Base.metadata,
    Column("transaction_id", ForeignKey("transaction.id", ondelete="CASCADE"), primary_key=True),
    Column("category_id", ForeignKey("category.id", ondelete="CASCADE"), primary_key=True)
)