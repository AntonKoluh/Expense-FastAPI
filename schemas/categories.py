from pydantic import BaseModel, ConfigDict

class CategoryWrite(BaseModel):
    name: str
    limit: int | None = None
    

class CategoryRead(CategoryWrite):
    user_id: int

    model_config = ConfigDict(from_attributes=True)