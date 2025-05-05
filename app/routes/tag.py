from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.models.tag import Tag
from app.models.note import Note
from app.schemas.tag import TagCreate, TagResponse, TagWithNotes
from app.helpers.auth import get_current_user
from app.models.user import User

router = APIRouter(
  prefix="/tags",
  tags=["Tags"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=TagResponse)
def create_tag(
  tag: TagCreate,
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_user)
):
  # Check if tag with same name already exists
  db_tag = db.query(Tag).filter(Tag.name == tag.name).first()
  if db_tag:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail="Tag with this name already exists"
    )
  
  new_tag = Tag(**tag.model_dump())
  db.add(new_tag)
  db.commit()
  db.refresh(new_tag)
  return new_tag

@router.get("/", response_model=List[TagResponse])
def get_tags(
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_user)
):
  tags = db.query(Tag).all()
  return tags

@router.get("/{tag_id}", response_model=TagWithNotes)
def get_tag(
  tag_id: str,
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_user)
):
  tag = db.query(Tag).filter(Tag.id == tag_id).first()
  if not tag:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="Tag not found"
    )
  return tag

@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tag(
  tag_id: str,
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_user)
):
  tag = db.query(Tag).filter(Tag.id == tag_id).first()
  if not tag:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="Tag not found"
    )
  
  db.delete(tag)
  db.commit()
  return None

@router.post("/{tag_id}/notes/{note_id}", status_code=status.HTTP_200_OK)
def add_tag_to_note(
  tag_id: str,
  note_id: str,
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_user)
):
  tag = db.query(Tag).filter(Tag.id == tag_id).first()
  if not tag:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="Tag not found"
    )
  
  note = db.query(Note).filter(Note.id == note_id).first()
  if not note:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="Note not found"
    )
  
  # Check if user owns the note
  if note.userId != current_user.id:
    raise HTTPException(
      status_code=status.HTTP_403_FORBIDDEN,
      detail="Not authorized to modify this note"
    )
  
  if tag in note.tags:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail="Note already has this tag"
    )
  
  note.tags.append(tag)
  db.commit()
  return {"message": "Tag added to note successfully"}

@router.delete("/{tag_id}/notes/{note_id}", status_code=status.HTTP_200_OK)
def remove_tag_from_note(
  tag_id: str,
  note_id: str,
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_user)
):
  tag = db.query(Tag).filter(Tag.id == tag_id).first()
  if not tag:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="Tag not found"
    )
  
  note = db.query(Note).filter(Note.id == note_id).first()
  if not note:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="Note not found"
    )
  
  # Check if user owns the note
  if note.userId != current_user.id:
    raise HTTPException(
      status_code=status.HTTP_403_FORBIDDEN,
      detail="Not authorized to modify this note"
    )
  
  if tag not in note.tags:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail="Note doesn't have this tag"
    )
  
  note.tags.remove(tag)
  db.commit()
  return {"message": "Tag removed from note successfully"} 