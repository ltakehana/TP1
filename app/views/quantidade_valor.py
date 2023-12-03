from app.schemas.produto_schema import ProdutoSchema

class QuantidadeValorView:
    @staticmethod
    def format_response(schema: ProdutoSchema):
        return({
            "quantidade": schema.quantidade_disponivel
        })