from sqlalchemy import Column, Integer, String
from app.database import Base

class FornecedorModel(Base):
    __tablename__ = "fornecedores"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    endereco = Column(String)
    telefone = Column(String)
