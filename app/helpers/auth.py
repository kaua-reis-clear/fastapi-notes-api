from typing import Annotated
from fastapi import Depends, HTTPException, Header, status
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import jwt
from app import models
from app.config.database import get_db
from app.config.settings import settings
from sqlalchemy.orm import Session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
  return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
  return pwd_context.verify(plain_password, hashed_password)


def create_access_token(user_id: str) -> str:
  expire = datetime.now(timezone.utc) + timedelta(minutes=15)
  payload = {
    'sub': user_id,
    'exp': expire,
  }
  encoded_jwt = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
  return encoded_jwt

def verify_access_token(token: str) -> str:
  try:
    payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    user_id = payload.get('sub')
    if user_id is None:
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')    
    return user_id
  except jwt.PyJWTError as e:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')
  
  
def get_current_user(authorization: Annotated[str | None, Header()] = None, db: Session = Depends(get_db)):
  if not authorization:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authorization header missing')
  
  token = authorization.split(' ')[1]

  user_id = verify_access_token(token)

  user = db.query(models.User).filter(models.User.id == user_id).first()
  if not user:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')

  return user
