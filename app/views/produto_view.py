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
            "filial_id": schema.filial_id,
        }