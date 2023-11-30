from pydantic import BaseModel

class FornecedorSchema(BaseModel):
    nome: str
    endereco: str
    telefone: str
