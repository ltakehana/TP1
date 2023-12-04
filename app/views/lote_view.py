from app.schemas.lote_schema import LoteSchema

class LoteView:
    @staticmethod
    def format_response(schema: LoteSchema):
        return {
            "id": schema.id,
            "quantidade": schema.quantidade,
            "produto_id": schema.produto_id,
            "data_validade": schema.data_validade
        }
        
        