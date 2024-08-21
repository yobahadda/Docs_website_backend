from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Payment as PaymentModel
from models.payment import Payment
from schemas import payment as payment_schema
from config.database import SessionLocal

router = APIRouter(
    prefix="/payment",
    tags=["payment"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=payment_schema.Payment)
def create_payment(payment: payment_schema.PaymentCreate, db: Session = Depends(get_db)):
    db_payment = PaymentModel(
        montant=payment.montant,
        devise=payment.devise,
        transaction_id=payment.transaction_id,
        etat_cout=payment.etat_cout,
        date_paiement=payment.date_paiement,  # Ensure this is stored as a date object in DB
        id_user=payment.id_user,
        id_offre=payment.id_offre
    )
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    
    # Convert date_paiement to string if needed
    db_payment_dict = db_payment.__dict__.copy()
    db_payment_dict['date_paiement'] = db_payment.date_paiement.isoformat()

    return db_payment_dict
    
@router.get("/", response_model=List[payment_schema.Payment])
def get_completed_payments(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    payments = db.query(PaymentModel).filter(PaymentModel.etat_cout == 'confirmed').offset(skip).limit(limit).all()
    if not payments:
        raise HTTPException(status_code=404, detail="No completed payments found")
    
    # Manually convert date_paiement to a string
    for payment in payments:
        payment.date_paiement = payment.date_paiement.isoformat()

    return payments