from pydantic import BaseModel


class TransacaoSchema(BaseModel):
    tipo: str  # ajustes, devoluções e vendas
    quantidade: int
    codigo_barras: str
    filial_id: int


class TransacaoRecebimentoSchema(BaseModel):
    quantidade: int
    codigo_barras: str
    fornecedor_id: int
    filial_id: int


class TransacaoTransferenciaSchema(BaseModel):
    quantidade: int
    codigo_barras: str
    filial_origem: int
    filial_destino: int
