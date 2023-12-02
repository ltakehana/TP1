from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class ProdutoModel(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String, index=True)
    codigo_barras = Column(String, index=True, unique=True)
    custo = Column(Float)
    preco_venda = Column(Float)
    quantidade_disponivel = Column(Integer)

    categoria_id = Column(Integer, ForeignKey("categorias.id"))
    categoria = relationship("CategoriaModel", back_populates="produtos")
