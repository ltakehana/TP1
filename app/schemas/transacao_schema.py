from pydantic import BaseModel

class TransacaoSchema(BaseModel):
    tipo: str
    quantidade: int
    produto_id: int
