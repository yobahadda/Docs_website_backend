# routers/docs_offre.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import DocsOffre
from config.database import SessionLocal

router = APIRouter(
    prefix="/docs_offres",
    tags=["docs_offres"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def read_docs_offres(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    docs_offres = db.query(DocsOffre).offset(skip).limit(limit).all()
    return docs_offres

@router.post("/")
def create_docs_offre(docs_offre: DocsOffre, db: Session = Depends(get_db)):
    db.add(docs_offre)
    db.commit()
    db.refresh(docs_offre)
    return docs_offre

@router.get("/{docs_offre_id}")
def read_docs_offre(docs_offre_id: int, db: Session = Depends(get_db)):
    docs_offre = db.query(DocsOffre).filter(DocsOffre.id_docs_offre == docs_offre_id).first()
    if docs_offre is None:
        raise HTTPException(status_code=404, detail="DocsOffre not found")
    return docs_offre

@router.put("/{docs_offre_id}")
def update_docs_offre(docs_offre_id: int, updated_docs_offre: DocsOffre, db: Session = Depends(get_db)):
    docs_offre = db.query(DocsOffre).filter(DocsOffre.id_docs_offre == docs_offre_id).first()
    if docs_offre is None:
        raise HTTPException(status_code=404, detail="DocsOffre not found")
    for key, value in updated_docs_offre.dict().items():
        setattr(docs_offre, key, value)
    db.commit()
    db.refresh(docs_offre)
    return docs_offre

@router.delete("/{docs_offre_id}")
def delete_docs_offre(docs_offre_id: int, db: Session = Depends(get_db)):
    docs_offre = db.query(DocsOffre).filter(DocsOffre.id_docs_offre == docs_offre_id).first()
    if docs_offre is None:
        raise HTTPException(status_code=404, detail="DocsOffre not found")
    db.delete(docs_offre)
    db.commit()
    return {"message": "DocsOffre deleted successfully"}
