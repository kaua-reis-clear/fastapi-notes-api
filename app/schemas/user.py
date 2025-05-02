from datetime import datetime
from pydantic import BaseModel, EmailStr
from uuid import UUID
  
class UserCreate(BaseModel):
  email: EmailStr
  password: str

class UserOut(BaseModel):
  id: UUID
  email: EmailStr
  createdAt: datetime

  class Config:
    from_attributes = True
