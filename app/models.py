from .database import Base
from sqlalchemy import TIMESTAMP, Column, String, Boolean
from sqlalchemy.sql import func
from fastapi_utils.guid_type import GUID, GUID_SERVER_DEFAULT_POSTGRESQL

class Note(Base):
  __tablename__ = 'notes'
  id = Column(GUID, primary_key=True,
              server_default=GUID_SERVER_DEFAULT_POSTGRESQL)
  title = Column(String, nullable=False)
  content = Column(String, nullable=False)
  imageUrl = Column(String, nullable=True)
  published = Column(Boolean, nullable=False, server_default='true')
  createdAt = Column(TIMESTAMP(timezone=True),
                     nullable=False, server_default=func.now())
  updatedAt = Column(TIMESTAMP(timezone=True),
                     default=None, onupdate=func.now())
  
  def __repr__(self) -> str:
    return self.title
  
  
  
class User(Base):
  __tablename__ = 'users'
  id = Column(GUID, primary_key=True,
              server_default=GUID_SERVER_DEFAULT_POSTGRESQL)
  email = Column(String, nullable=False, unique=True)
  password = Column(String, nullable=False)
  createdAt = Column(TIMESTAMP(timezone=True),
                     nullable=False, server_default=func.now())
  updatedAt = Column(TIMESTAMP(timezone=True),
                     default=None, onupdate=func.now())
  
  def __repr__(self) -> str:
    return self.email
