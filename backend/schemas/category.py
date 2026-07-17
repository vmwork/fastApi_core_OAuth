import uuid
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field

class CategoryBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    slug: str = Field(..., min_length=2, max_length=120)
    description: Optional[str] = Field(None, max_length=500)
    is_active: bool = True

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    slug: Optional[str] = Field(None, min_length=2, max_length=120)
    description: Optional[str] = Field(None, max_length=500)
    is_active: Optional[bool] = None

class ShowCategory(CategoryBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    blogs: List["ShowBlog"] = []  # ← Добавили

    class Config:
        from_attributes = True

from schemas.blog import ShowBlog
ShowCategory.model_rebuild()