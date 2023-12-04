from pydantic import BaseModel

class TransacaoSchema(BaseModel):
    tipo: str
    quantidade: int
    lote_id: int
