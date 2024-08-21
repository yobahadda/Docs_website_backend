# models/synthese.py
from sqlalchemy import Column, Integer, String, Date
from config.database import Base

class Synthese(Base):
    __tablename__ = "synthese"

    id_synthese = Column(Integer, primary_key=True, index=True)
    date_generation = Column(Date, nullable=False)
    chemin_synthese = Column(String(255), nullable=False)
    id_synthese_parent = Column(Integer, nullable=True)
