from typing import List
from app.config.database import Base
from sqlalchemy import TIMESTAMP, String, Uuid, Table, Column, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from fastapi_utils.guid_type import GUID_SERVER_DEFAULT_POSTGRESQL

# Association table for many-to-many relationship between Note and Tag
note_tags = Table(
  'note_tags',
  Base.metadata,
  Column('note_id', Uuid(as_uuid=False), ForeignKey('notes.id', ondelete='CASCADE')),
  Column('tag_id', Uuid(as_uuid=False), ForeignKey('tags.id', ondelete='CASCADE'))
)

class Tag(Base):
  __tablename__ = 'tags'
  
  id: Mapped[str] = mapped_column(Uuid(as_uuid=False), primary_key=True, server_default=GUID_SERVER_DEFAULT_POSTGRESQL)
  name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
  createdAt: Mapped[str] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
  
  # Relationship with Note model
  notes: Mapped[List['Note']] = relationship(secondary=note_tags, back_populates="tags")
  
  def __repr__(self) -> str:
    return self.name 