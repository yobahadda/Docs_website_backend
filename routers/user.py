# routers/user.py
from fastapi import APIRouter, Depends, HTTPException, logger
from sqlalchemy.orm import Session
from typing import List
from models import User as UserModel, Payment as PaymentModel, Offre as OffreModel
from schemas import user as user_schema, offre as offre_schema
from config.database import SessionLocal

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[user_schema.User])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(UserModel).offset(skip).limit(limit).all()
    return users

@router.get("/{user_id}", response_model=user_schema.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id_user == user_id).first()
    if user is None:
        logger.warning(f"User with ID {user_id} not found.")
        raise HTTPException(status_code=404, detail="User not found")
    logger.info(f"User with ID {user_id} retrieved successfully.")
    return user

@router.post("/", response_model=user_schema.User)
def create_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    db_user = UserModel(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/{user_id}", response_model=user_schema.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id_user == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=user_schema.User)
def update_user(user_id: int, updated_user: user_schema.UserCreate, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id_user == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in updated_user.dict().items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user

@router.delete("/{user_id}", response_model=user_schema.User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id_user == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return user

@router.get("/{user_id}/plan", response_model=offre_schema.Offre)
def get_user_plan(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id_user == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    latest_payment = db.query(PaymentModel).filter(PaymentModel.id_user == user_id).order_by(PaymentModel.date_paiement.desc()).first()
    if not latest_payment:
        raise HTTPException(status_code=404, detail="No payment found for user")

    offer = db.query(OffreModel).filter(OffreModel.id_offre == latest_payment.id_offre).first()
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found for user's payment")

    return offer
