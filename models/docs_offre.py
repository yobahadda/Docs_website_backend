# models/docs_offre.py
from sqlalchemy import Column, Integer
from config.database import Base

class DocsOffre(Base):
    __tablename__ = "docs_offre"

    id_document = Column(Integer, primary_key=True, nullable=False)
    id_offre = Column(Integer, primary_key=True, nullable=False)
