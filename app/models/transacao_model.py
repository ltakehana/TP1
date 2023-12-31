from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class TransacaoModel(Base):
    __tablename__ = "transacoes"

    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String, index=True)
    quantidade = Column(Integer)
    lote_id = Column(Integer, ForeignKey("lotes.id"))
    data = Column(DateTime, default=datetime.utcnow)
