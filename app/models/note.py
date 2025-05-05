from typing import Optional
from app.config.database import Base
from sqlalchemy import TIMESTAMP, String, Boolean, Uuid, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from fastapi_utils.guid_type import GUID_SERVER_DEFAULT_POSTGRESQL

class Note(Base):
  __tablename__ = 'notes'
  id: Mapped[str] = mapped_column(Uuid(as_uuid=False), primary_key=True, server_default=GUID_SERVER_DEFAULT_POSTGRESQL)
  title: Mapped[str] = mapped_column(String(100), nullable=False)
  content: Mapped[str] = mapped_column(String(100), nullable=False)
  published: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default='true')
  createdAt: Mapped[str] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
  updatedAt: Mapped[Optional[str]] = mapped_column(TIMESTAMP(timezone=True), default=None, onupdate=func.now())
  userId: Mapped[str] = mapped_column(ForeignKey('users.id'))
  user: Mapped['User'] = relationship(back_populates="notes")
  
  def __repr__(self) -> str:
    return self.title
