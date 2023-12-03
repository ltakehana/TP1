from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class FilialModel(Base):
    __tablename__ = "filiais"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    endereco = Column(String)
    telefone = Column(String)
