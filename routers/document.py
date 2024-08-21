# routers/document.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import document as document_model
from config.database import get_db
from schemas.document import DocumentCreate, Document

router = APIRouter()

@router.get("/{document_id}", response_model=Document)
def get_document(document_id: int, db: Session = Depends(get_db)):
    db_document = db.query(document_model.Document).filter(document_model.Document.id_document == document_id).first()
    if db_document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return db_document
