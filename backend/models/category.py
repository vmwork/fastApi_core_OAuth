from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.types import UUID  
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from db.base_class import Base
from models.blog_category import blog_categories 
from utils.uuid import generate_uuidv7  

class Category(Base):
    __tablename__ = "categories"

    id = Column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=generate_uuidv7, 
        index=True
    )
    name = Column(String(100), nullable=False, unique=True, index=True)
    slug = Column(String(120), nullable=False, unique=True, index=True)
    description = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    blogs = relationship("Blog", secondary=blog_categories, back_populates="categories")
