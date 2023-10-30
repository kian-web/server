from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from uuid import uuid1

from app.database import Base


class Teacher(Base):
    uuid = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid1)
    email = Column(String, unique=True, index=True)
    hashed_pass = Column(String)
    is_active = Column(Boolean, default=True)
    classes = relationship("Class", back_populates="teacher")
