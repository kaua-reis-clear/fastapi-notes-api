from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, UUID4

class TagBase(BaseModel):
  name: str

class TagCreate(TagBase):
  pass

class TagResponse(TagBase):
  id: UUID4
  createdAt: datetime
  updatedAt: Optional[datetime] = None
  
  class Config:
    from_attributes = True

class TagWithNotes(TagResponse):
  notes: List['NoteResponse']

class NoteResponse(BaseModel):
  id: UUID4
  title: str
  content: str
  published: bool
  createdAt: datetime
  updatedAt: Optional[datetime] = None
  
  class Config:
    from_attributes = True

# Update forward references
TagWithNotes.model_rebuild() 