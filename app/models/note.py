from app.config.database import Base
from sqlalchemy import TIMESTAMP, Column, String, Boolean
from sqlalchemy.sql import func
from fastapi_utils.guid_type import GUID, GUID_SERVER_DEFAULT_POSTGRESQL

class Note(Base):
  __tablename__ = 'notes'
  id = Column(GUID, primary_key=True,
              server_default=GUID_SERVER_DEFAULT_POSTGRESQL)
  title = Column(String, nullable=False)
  content = Column(String, nullable=False)
  published = Column(Boolean, nullable=False, server_default='true')
  createdAt = Column(TIMESTAMP(timezone=True),
                     nullable=False, server_default=func.now())
  updatedAt = Column(TIMESTAMP(timezone=True),
                     default=None, onupdate=func.now())
  
  def __repr__(self) -> str:
    return self.title
