# schemas/offre.py
from pydantic import BaseModel
from typing import Optional

class Offre(BaseModel):
    id_offre: int
    nom_offre: str
    nom_user: str
    description: str
    max_doc: int
    prix_offre: float
    id_offre_parent: Optional[int] = None

    class Config:
        orm_mode = True
