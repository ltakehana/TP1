from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class CategoriaModel(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True, unique=True)

    produtos = relationship("ProdutoModel", back_populates="categoria")
