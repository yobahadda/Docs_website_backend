# routers/concerne.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Concerne
from config.database import SessionLocal

router = APIRouter(
    prefix="/concernes",
    tags=["concernes"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def read_concernes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    concernes = db.query(Concerne).offset(skip).limit(limit).all()
    return concernes

@router.post("/")
def create_concerne(concerne: Concerne, db: Session = Depends(get_db)):
    db.add(concerne)
    db.commit()
    db.refresh(concerne)
    return concerne

@router.get("/{concerne_id}")
def read_concerne(concerne_id: int, db: Session = Depends(get_db)):
    concerne = db.query(Concerne).filter(Concerne.id_concerne == concerne_id).first()
    if concerne is None:
        raise HTTPException(status_code=404, detail="Concerne not found")
    return concerne

@router.put("/{concerne_id}")
def update_concerne(concerne_id: int, updated_concerne: Concerne, db: Session = Depends(get_db)):
    concerne = db.query(Concerne).filter(Concerne.id_concerne == concerne_id).first()
    if concerne is None:
        raise HTTPException(status_code=404, detail="Concerne not found")
    for key, value in updated_concerne.dict().items():
        setattr(concerne, key, value)
    db.commit()
    db.refresh(concerne)
    return concerne

@router.delete("/{concerne_id}")
def delete_concerne(concerne_id: int, db: Session = Depends(get_db)):
    concerne = db.query(Concerne).filter(Concerne.id_concerne == concerne_id).first()
    if concerne is None:
        raise HTTPException(status_code=404, detail="Concerne not found")
    db.delete(concerne)
    db.commit()
    return {"message": "Concerne deleted successfully"}
