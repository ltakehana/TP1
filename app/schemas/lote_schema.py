from pydantic import BaseModel

class LoteSchema(BaseModel):
    id: int
    quantidade: int
    produto_id: int
    data_validade: str

    