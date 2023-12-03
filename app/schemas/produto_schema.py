from pydantic import BaseModel

class ProdutoSchema(BaseModel):
    descricao: str
    codigo_barras: str
    custo: float
    preco_venda: float
    quantidade_disponivel: int
    filial_id: int
    quantidade_disponivel: int
