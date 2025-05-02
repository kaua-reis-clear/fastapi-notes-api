
from fastapi import APIRouter, Depends, HTTPException, Header, Response, status
from sqlalchemy.orm import Session
from app.config.database import get_db
from app import models, schemas
from app.helpers.auth import create_access_token, get_current_user, hash_password, verify_password

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
  
  access_token = create_access_token(user.id.__str__())
  
  response.headers['Access-Token'] = access_token

  return user

@router.get('/me', response_model=schemas.user.UserOut)
def get_me(current_user: models.User = Depends(get_current_user)):
  return current_user
