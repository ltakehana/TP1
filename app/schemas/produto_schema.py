from pydantic import BaseModel, Field

class ProdutoSchema(BaseModel):
    descricao: str
    codigo_barras: str
    custo: float
    preco_venda: float
    quantidade_disponivel: int
    quantidade_minima: int = Field(default=1)
    fornecedor_id: int


class ProdutoCreationSchema(ProdutoSchema):
    lote: int
    validade: str
