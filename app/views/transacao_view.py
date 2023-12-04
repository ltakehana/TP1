from app.schemas.transacao_schema import TransacaoSchema
from app.models.transacao_model import TransacaoModel

class TransacaoView:
    def format_response(self, transacao: TransacaoModel) -> TransacaoSchema:
        return TransacaoSchema(
            id=transacao.id,
            tipo=transacao.tipo,
            quantidade=transacao.quantidade,
            lote_id=transacao.lote_id,
            data_criacao=transacao.data_criacao
        )
