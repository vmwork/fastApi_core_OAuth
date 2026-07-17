import uuid
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, field_validator


class CreateBlog(BaseModel):
    title: str
    slug: str
    content: Optional[str] = None
    is_active: bool = False
    published: bool = False
    categories_id: Optional[List[uuid.UUID]] = []

    @field_validator("slug")
    def generate_slug(cls, v, info):
        if v:
            return v
        title = info.data.get("title")
        if title:
            return title.replace(" ", "-").lower()
        return v
 

class ShowBlog(BaseModel):
    id: uuid.UUID
    title: str
    slug: str
    content: Optional[str]
    is_active: bool
    published: bool
    published_at: Optional[datetime]
    created_at: datetime
    updated_at: Optional[datetime]
    author_id: uuid.UUID
    categories: List["ShowCategory"] = [] 

    class Config:
        from_attributes = True


class UpdateBlog(BaseModel):
    title: Optional[str] = None
    slug: Optional[str] = None
    content: Optional[str] = None
    is_active: Optional[bool] = None
    published: Optional[bool] = None
    categories_id: Optional[List[uuid.UUID]] = None

    @field_validator("slug")
    def generate_slug(cls, v, info):
        if v:
            return v
        title = info.data.get("title")
        if title:
            return title.replace(" ", "-").lower()
        return v


from schemas.category import ShowCategory
ShowBlog.model_rebuild()