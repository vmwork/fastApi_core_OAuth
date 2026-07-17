import uuid
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=4)


class ShowUser(BaseModel):
    id: uuid.UUID
    email: EmailStr
    is_active: bool

    class Config: 
        from_attributes = True
