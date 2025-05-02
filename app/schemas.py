from datetime import datetime
from typing import List
from pydantic import BaseModel, EmailStr
from uuid import UUID

class NoteBaseSchema(BaseModel):
  id: str | None = None
  title: str
  content: str
  imageUrl: str | None = None
  published: bool = True
  createdAt: datetime | None = None
  updatedAt: datetime | None = None
  
  class Config:
    from_attributes = True
    validate_by_name = True
    arbitrary_types_allowed = True
    
class ListNoteResponse(BaseModel):
  status: str
  results: str
  notes: List[NoteBaseSchema]
  
  
class UserCreate(BaseModel):
  email: EmailStr
  password: str

class UserOut(BaseModel):
  id: UUID
  email: EmailStr
  createdAt: datetime

  class Config:
    from_attributes = True
