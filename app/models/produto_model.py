from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.fornecedor_model import FornecedorModel

class ProdutoModel(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    codigo_barras = Column(String, index=True)
    descricao = Column(String)
    custo = Column(Float)
    preco_venda = Column(Float)
    quantidade_disponivel = Column(Integer)
    quantidade_minima = Column(Integer)

    fornecedor_id = Column(Integer, ForeignKey(FornecedorModel.id))
    fornecedor = relationship("FornecedorModel", back_populates="produtos")
