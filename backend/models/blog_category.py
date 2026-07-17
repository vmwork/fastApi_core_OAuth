from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.types import UUID  
from db.base_class import Base

blog_categories = Table(
    "blog_categories",
    Base.metadata,
    Column(
        "blog_id", 
        UUID(as_uuid=True), 
        ForeignKey("blogs.id", ondelete="CASCADE"), 
        primary_key=True
    ),
    Column(
        "category_id", 
        UUID(as_uuid=True), 
        ForeignKey("categories.id", ondelete="CASCADE"), 
        primary_key=True
    )
)
