from typing import Optional
from app.config.database import Base
from sqlalchemy import TIMESTAMP, String, Uuid
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column
from fastapi_utils.guid_type import GUID_SERVER_DEFAULT_POSTGRESQL

class User(Base):
  __tablename__ = 'users'
  id: Mapped[str] = mapped_column(Uuid(as_uuid=False), primary_key=True, server_default=GUID_SERVER_DEFAULT_POSTGRESQL)
  email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
  username: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
  password: Mapped[str] = mapped_column(String(100), nullable=False)
  createdAt: Mapped[str] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
  updatedAt: Mapped[Optional[str]] = mapped_column(TIMESTAMP(timezone=True), default=None, onupdate=func.now())
  
  def __repr__(self) -> str:
    return self.email