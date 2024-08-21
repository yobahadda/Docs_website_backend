# schemas/payment.py
from pydantic import BaseModel

class PaymentCreate(BaseModel):
    montant: float
    devise: str
    transaction_id: str
    etat_cout: str
    date_paiement: str
    id_user: int
    id_offre: int

class Payment(BaseModel):
    id_payment: int
    montant: float
    devise: str
    transaction_id: str
    etat_cout: str
    date_paiement: str
    id_user: int
    id_offre: int

    class Config:
        orm_mode = True
