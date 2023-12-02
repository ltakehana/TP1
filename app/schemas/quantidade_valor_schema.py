from pydantic import BaseModel

class QuantidadeValorSchema(BaseModel):
    produto_id: int
    quantidade: int
    valor_total: float
