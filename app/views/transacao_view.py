from app.schemas.transacao_schema import TransacaoRecebimentoSchema, TransacaoSchema, TransacaoTransferenciaSchema

class TransacaoView:
    @staticmethod
    def format_response(schema: TransacaoSchema):
        return {
            "tipo": schema.tipo,
            "quantidade": schema.quantidade,
            "produto_id": schema.produto_id,
            "filial_id": schema.filial_id,
        }

class TransacaoRecebimentoView:
    @staticmethod
    def format_response(schema: TransacaoRecebimentoSchema):
        return {
            "quantidade": schema.quantidade,
            "produto_id": schema.produto_id,
            "filial_id": schema.filial_id,
            "fornecedor_id": schema.fornecedor_id,
        }

class TransacaoTransferenciaView:
    @staticmethod
    def format_response(schema: TransacaoTransferenciaSchema):
        return {
            "quantidade": schema.quantidade,
            "produto_id": schema.produto_id,
            "filial_origem": schema.filial_origem,
            "filial_destino": schema.filial_destino,
        }