from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class TransacaoModel(Base):
    __tablename__ = "transacoes"

    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String, index=True)
    quantidade = Column(Integer)
    produto_id = Column(Integer, ForeignKey("produtos.id"))
    filial_id = Column(Integer, ForeignKey("filiais.id"))
    data = Column(DateTime, default=datetime.utcnow)


class TransacaoRecebimentoModel(Base):
    __tablename__ = "transacoesRecebimento"

    id = Column(Integer, primary_key=True, index=True)
    quantidade = Column(Integer)
    produto_id = Column(Integer, ForeignKey("produtos.id"))
    data = Column(DateTime, default=datetime.utcnow)
    fornecedor_id = Column(Integer, ForeignKey("fornecedores.id"))
    filial_id = Column(Integer, ForeignKey("filiais.id"))


class TransacaoTransferenciaModel(Base):
    __tablename__ = "transacoesTransferencia"
    id = Column(Integer, primary_key=True, index=True)
    quantidade = Column(Integer)
    produto_origem = Column(Integer, ForeignKey("produtos.id"))
    produto_destino = Column(Integer, ForeignKey("produtos.id"))
    data = Column(DateTime, default=datetime.utcnow)
    filial_origem = Column(Integer, ForeignKey("filiais.id"))
    filial_destino = Column(Integer, ForeignKey("filiais.id"))
