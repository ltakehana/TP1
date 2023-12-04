from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class LoteModel(Base):
    __tablename__ = "lotes"

    id = Column(Integer, primary_key=True, index=True)
    quantidade = Column(Integer)
    produto_id = Column(Integer, ForeignKey("produtos.id"))
    data_validade = Column(String)
