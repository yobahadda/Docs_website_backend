# models/document.py
from sqlalchemy import Column, Integer, String, Date
from config.database import Base

class Document(Base):
    __tablename__ = "document"

    id_document = Column(Integer, primary_key=True, index=True)
    nom_document = Column(String(100), nullable=False)
    type_document = Column(String(100), nullable=False)
    date_upload = Column(Date, nullable=False)
    id_document_parent = Column(Integer, nullable=True)
