from pydantic import BaseModel
from datetime import date

class AnalyseBase(BaseModel):
    date_analyse: date
    result: str

class AnalyseCreate(AnalyseBase):
    id_document: int

class Analyse(AnalyseBase):
    id_analyse: int

    class Config:
        orm_mode = True