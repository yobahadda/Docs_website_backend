# models/analyse.py
from sqlalchemy import Column, Integer, String, Date
from config.database import Base

class Analyse(Base):
    __tablename__ = "analyse"

    id_analyse = Column(Integer, primary_key=True, index=True)
    date_analyse = Column(Date, nullable=False)
    result = Column(String(255), nullable=False)
    id_document = Column(Integer, nullable=False)
