from pydantic import BaseModel, ConfigDict


class CategoryRead(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class TransactionWrite(BaseModel):
    name: str
    amount: int
    categories: list[str]


class TransactionRead(BaseModel):
    id: int
    name: str
    amount: int
    user_id: int
    categories: list[CategoryRead]

    model_config = ConfigDict(from_attributes=True)