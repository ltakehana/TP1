from pydantic import BaseModel


class TransacaoSchema(BaseModel):
    tipo: str  # ajustes, devoluções e vendas
    quantidade: int
    produto_id: int
    filial_id: int


class TransacaoRecebimentoSchema(BaseModel):
    quantidade: int
    produto_id: int
    fornecedor_id: int
    filial_id: int


class TransacaoTransferenciaSchema(BaseModel):
    quantidade: int
    produto_id: int
    filial_origem: int
    filial_destino: int
