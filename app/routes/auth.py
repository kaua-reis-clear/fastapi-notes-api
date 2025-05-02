from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Header, Response, status
import jwt
from sqlalchemy.orm import Session
from app.config.settings import settings
from app.config.database import get_db
from app import models, schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
  return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
  return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

router = APIRouter()

@router.post('/sign_up', response_model=schemas.user.UserOut, status_code=201)
def sign_up(payload: schemas.user.UserCreate, db: Session = Depends(get_db)):
  hashed_password = hash_password(payload.password)
  new_user = models.User(email=payload.email, password=hashed_password)
  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  return new_user

@router.post('/login', response_model=schemas.user.UserOut)
def login(payload: schemas.user.UserCreate, response: Response, db: Session = Depends(get_db)):
  user_query = db.query(models.User).filter(models.User.email == payload.email)
  user = user_query.first()
  
  if not user:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User not found')

  if not verify_password(payload.password, user.password):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid email or password')
  
  access_token = create_access_token(data={"sub": user.id.__str__()})
  
  response.headers['Access-Token'] = access_token

  return user

def get_current_user(authorization: Annotated[str | None, Header()] = None, db: Session = Depends(get_db)):
  if not authorization:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not authenticated')
  
  token = authorization.split(' ')[1]

  try:
    payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    user_id = payload.get('sub')
    if user_id is None:
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')
  except jwt.PyJWTError as e:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')

  user = db.query(models.User).filter(models.User.id == user_id).first()
  if not user:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')

  return user

@router.get('/me', response_model=schemas.user.UserOut)
def get_me(current_user: models.User = Depends(get_current_user)):
  return current_user
