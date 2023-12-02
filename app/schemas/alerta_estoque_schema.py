from pydantic import BaseModel

class AlertaEstoqueSchema(BaseModel):
    produto_id: int
    mensagem: str
