# models/user.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from config.database import Base

class User(Base):
    __tablename__ = "user"

    id_user = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    password = Column(String(100))
    nom_user = Column(String(100))
    prenom = Column(String(100))
    role = Column(String(50))

    payments = relationship("Payment", back_populates="user")
