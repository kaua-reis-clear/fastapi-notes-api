from app import schemas, models
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter, Response
from app.config.database import get_db
from app.helpers.auth import get_current_user

router = APIRouter()

@router.get('')
def get_notes(db: Session = Depends(get_db), current_user = Depends(get_current_user), limit: int = 10, page: int = 1, search: str = ''):
  skip = (page - 1) * limit
  
  notes = db.query(models.Note).filter(
    models.Note.title.contains(search), models.Note.userId == current_user.id).limit(limit).offset(skip).all()
  
  return {'status': 'success', 'results': len(notes), 'notes': notes}

@router.post('', status_code=status.HTTP_201_CREATED)
def create_note(payload: schemas.note.NoteBaseSchema, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
  new_note = models.Note(**payload.model_dump(), userId=current_user.id)
  db.add(new_note)
  db.commit()
  db.refresh(new_note)
  return {'status': 'success', 'note': new_note}

@router.patch('/{noteId}')
def update_note(noteId: str, payload: schemas.note.NoteBaseSchema, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
  note_query = db.query(models.Note).filter(models.Note.id == noteId, models.Note.userId==current_user.id)
  db_note = note_query.first()
  
  if not db_note:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'No note with this id: {noteId} found')
    
  update_data = payload.model_dump(exclude_unset=True)
  note_query.update(update_data, synchronize_session=False)
  db.commit()
  db.refresh(db_note)
  return {'status': 'success', 'note': db_note}

@router.get('/{noteId}')
def get_note(noteId: str, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
  note = db.query(models.Note).filter(models.Note.id == noteId, models.Note.userId==current_user.id).first()
  if not note:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'No note with this id: {noteId} found')
    
  return {'status': 'success', 'note': note}

@router.delete('/{noteId}', status_code=status.HTTP_204_NO_CONTENT)
def delete_note(noteId: str, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
  note_query = db.query(models.Note).filter(models.Note.id == noteId, models.Note.userId==current_user.id)
  note = note_query.first()
  if not note:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'No note with this id: {noteId} found')
    
  note_query.delete(synchronize_session=False)
  db.commit()
  
  return Response(status_code=status.HTTP_204_NO_CONTENT)
