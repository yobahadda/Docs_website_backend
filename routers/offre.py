# routers/offre.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from config.database import SessionLocal
from models import offre as offre_model
from schemas import offre as offre_schema

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[offre_schema.Offre])
def read_offres(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    offres = db.query(offre_model.Offre).offset(skip).limit(limit).all()
    return offres
