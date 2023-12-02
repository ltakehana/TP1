from sqlalchemy import Column, Integer, Float, ForeignKey
from app.database import Base

class QuantidadeValorModel(Base):
    __tablename__ = "quantidade_valor"

    id = Column(Integer, primary_key=True, index=True)
    produto_id = Column(Integer, ForeignKey("produtos.id"))
    quantidade = Column(Integer)
    valor_total = Column(Float)
