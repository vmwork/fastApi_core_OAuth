import uuid
from utils.uuid import generate_uuidv7
from db.base_class import Base
from sqlalchemy import Boolean, Column, String
from sqlalchemy.types import UUID
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "user"

    id = Column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=generate_uuidv7,
        index=True
    )
    
    email = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
    is_superuser = Column(Boolean(), default=False)
    is_active = Column(Boolean(), default=True)
    
    blogs = relationship("Blog", back_populates="author")
