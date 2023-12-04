from app.schemas.produto_schema import ProdutoSchema

class ProdutoView:
    @staticmethod
    def format_response(schema: ProdutoSchema):
        return {
            "descricao": schema.descricao,
            "codigo_barras": schema.codigo_barras,
            "custo": schema.custo,
            "preco_venda": schema.preco_venda,
            "quantidade_disponivel": schema.quantidade_disponivel,
            "quantidade_minima": schema.quantidade_minima,
            "fornecedor_id": schema.fornecedor_id
        }
