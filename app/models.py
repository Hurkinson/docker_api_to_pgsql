from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from database import Base
from typing import Optional
from pydantic import BaseModel

# ============================ sqlalchemy model ==========> db interactions

class Commune(Base):
    __tablename__ = 'communes'
    id = Column(Integer, primary_key=True)
    code_postal = Column(String)
    nom_commune_complet = Column(String)
    departement = Column(String)
    code_geoloc = Column(String)

# ============================ pydantic model =============> i/o fastapi
    
class CommuneBase(BaseModel):
    code_postal: str
    nom_commune_complet: str
    departement: str
    code_geoloc: Optional[str] = None

class CommuneCreate(CommuneBase):
    pass

class CommuneModel(CommuneBase):
    id: int

    class Config:
        from_attributes = True
