# models/offre.py
from sqlalchemy import Column, Integer, String, Text, DECIMAL
from config.database import Base
from sqlalchemy.orm import relationship

class Offre(Base):
    __tablename__ = "offre"

    id_offre = Column(Integer, primary_key=True, index=True)
    nom_offre = Column(String(100))
    nom_user = Column(String(100))
    description = Column(Text)
    max_doc = Column(Integer)
    prix_offre = Column(DECIMAL(10, 2))
    id_offre_parent = Column(Integer, nullable=True)

    payments = relationship("Payment", back_populates="offre")
