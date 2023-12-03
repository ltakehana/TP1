from pydantic import BaseModel

class FilialSchema(BaseModel):
    nome: str
    endereco: str
    telefone: str
