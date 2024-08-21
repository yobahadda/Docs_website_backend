from sqlalchemy import Column, Integer
from config.database import Base

class Concerne(Base):
    __tablename__ = "concerne"

    id_user = Column(Integer, primary_key=True)
    id_document = Column(Integer, primary_key=True)