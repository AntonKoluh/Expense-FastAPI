from pydantic import BaseModel, ConfigDict

class UserRead(BaseModel):
    username: str
    is_staff: bool = False

    model_config = ConfigDict(from_attributes=True)

class UserCreate(UserRead):
    password: str

class UserLoginRespose(BaseModel):
    access_token: str

class UserLoginPost(BaseModel):
    username: str
    password: str