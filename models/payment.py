# models.py

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base

class Payment(Base):
    __tablename__ = 'payment'
    
    id_payment = Column(Integer, primary_key=True, index=True)
    montant = Column(Float, nullable=False)
    devise = Column(String, nullable=False)
    transaction_id = Column(String, nullable=False)
    etat_cout = Column(String, nullable=False)
    date_paiement = Column(DateTime, nullable=False)
    id_user = Column(Integer, ForeignKey('user.id_user'), nullable=False)
    id_offre = Column(Integer, ForeignKey('offre.id_offre'), nullable=False)

    user = relationship("User", back_populates="payments")
    offre = relationship("Offre", back_populates="payments")
