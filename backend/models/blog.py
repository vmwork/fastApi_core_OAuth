from datetime import datetime, timezone
import uuid

from db.base_class import Base
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, Text
from sqlalchemy.types import UUID 
from sqlalchemy.orm import relationship

# Импортируем связующую таблицу
from models.blog_category import blog_categories
from utils.uuid import generate_uuidv7  


class Blog(Base):
    __tablename__ = "blogs"
    
    id = Column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=generate_uuidv7, 
        index=True
    )
    title = Column(String, nullable=False)
    slug = Column(String, nullable=False, unique=True)
    content = Column(Text, nullable=True)
    
    author_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    author = relationship("User", back_populates="blogs")
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    is_active = Column(Boolean, default=False)
    published = Column(Boolean, default=False)
    published_at = Column(DateTime, nullable=True)
    
    categories = relationship("Category", secondary=blog_categories, back_populates="blogs")
