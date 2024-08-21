# routers/synthese.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Synthese
from config.database import SessionLocal

router = APIRouter(
    prefix="/syntheses",
    tags=["syntheses"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def read_syntheses(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    syntheses = db.query(Synthese).offset(skip).limit(limit).all()
    return syntheses

@router.post("/")
def create_synthese(synthese: Synthese, db: Session = Depends(get_db)):
    db.add(synthese)
    db.commit()
    db.refresh(synthese)
    return synthese

@router.get("/{synthese_id}")
def read_synthese(synthese_id: int, db: Session = Depends(get_db)):
    synthese = db.query(Synthese).filter(Synthese.id_synthese == synthese_id).first()
    if synthese is None:
        raise HTTPException(status_code=404, detail="Synthese not found")
    return synthese

@router.put("/{synthese_id}")
def update_synthese(synthese_id: int, updated_synthese: Synthese, db: Session = Depends(get_db)):
    synthese = db.query(Synthese).filter(Synthese.id_synthese == synthese_id).first()
    if synthese is None:
        raise HTTPException(status_code=404, detail="Synthese not found")
    for key, value in updated_synthese.dict().items():
        setattr(synthese, key, value)
    db.commit()
    db.refresh(synthese)
    return synthese

@router.delete("/{synthese_id}")
def delete_synthese(synthese_id: int, db: Session = Depends(get_db)):
    synthese = db.query(Synthese).filter(Synthese.id_synthese == synthese_id).first()
    if synthese is None:
        raise HTTPException(status_code=404, detail="Synthese not found")
    db.delete(synthese)
    db.commit()
    return {"message": "Synthese deleted successfully"}
