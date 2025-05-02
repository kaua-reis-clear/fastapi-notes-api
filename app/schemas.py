from datetime import datetime
from typing import List
from pydantic import BaseModel

class NoteBaseSchema(BaseModel):
  id: str | None = None
  title: str
  content: str
  imageUrl: str | None = None
  published: bool = True
  createdAt: datetime | None = None
  updatedAt: datetime | None = None
  
  class Config:
    orm_mode = True
    allow_population_by_field_name = True
    arbitrary_types_allowed = True
    
class ListNoteResponse(BaseModel):
  status: str
  results: str
  notes: List[NoteBaseSchema]
