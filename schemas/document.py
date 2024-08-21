from pydantic import BaseModel
from datetime import date

class DocumentBase(BaseModel):
    nom_document: str
    type_document: str
    date_upload: date

class DocumentCreate(DocumentBase):
    pass

class Document(DocumentBase):
    id_document: int
    id_document_parent: int = None

    class Config:
        orm_mode = True