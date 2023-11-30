from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime
from app.database import Base

class AlertaEstoqueModel(Base):
    __tablename__ = "alertas_estoque"

    id = Column(Integer, primary_key=True, index=True)
    produto_id = Column(Integer, ForeignKey("produtos.id"))
    mensagem = Column(String)
    data = Column(DateTime, default=datetime.utcnow)
