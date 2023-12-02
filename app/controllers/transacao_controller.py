from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.schemas.transacao_schema import TransacaoSchema, TransacaoCreationSchema
from app.models.transacao_model import TransacaoModel
from app.models.lote_model import LoteModel
from app.models.produto_model import ProdutoModel
from app.views.transacao_view import TransacaoView
from app.exceptions import CampoObrigatorioException, ValorInvalidoException

class TransacaoController:
    def __init__(self):
        self.transacao_view = TransacaoView()

    def create_transacao(self, db: Session, tipo, transacao: TransacaoCreationSchema):
        try:
            if (transacao.lote_id <= 0) or (transacao.quantidade<=0 and tipo!="ajuste"):
                raise ValorInvalidoException("A quantidade e o lote devem ser maiores que zero.")

            if not tipo:
                raise CampoObrigatorioException("O campo 'tipo' é obrigatório.")

            transacao_db = TransacaoModel(**transacao.dict())
            db.add(transacao_db)
            db.commit()
            db.refresh(transacao_db)

            if tipo == 'venda' or tipo=='transferencia':
                lote_db = db.query(LoteModel).filter(LoteModel.id == transacao.lote_id).first()

                if lote_db is None:
                    raise CampoObrigatorioException("Lote não encontrado.")

                if lote_db.quantidade < transacao.quantidade:
                    raise ValorInvalidoException("Quantidade de venda maior do que a disponível no lote.")

                lote_db.quantidade -= transacao.quantidade
                db.commit()
                db.refresh(lote_db)

                produto_db = db.query(ProdutoModel).filter(ProdutoModel.id == lote_db.produto_id).first()

                if produto_db is None:
                    raise CampoObrigatorioException("Produto associado ao lote não encontrado.")

                if produto_db.quantidade_disponivel < transacao.quantidade:
                    raise ValorInvalidoException("Quantidade de venda maior do que a disponível no produto.")

                produto_db.quantidade_disponivel -= transacao.quantidade
                db.commit()
                db.refresh(produto_db)

            if tipo == 'recebimento' or tipo=='devolucao' or tipo=='ajuste':
                lote_db = db.query(LoteModel).filter(LoteModel.id == transacao.lote_id).first()

                if lote_db is None:
                    raise CampoObrigatorioException("Lote não encontrado.")

                produto_db = db.query(ProdutoModel).filter(ProdutoModel.id == lote_db.produto_id).first()

                if produto_db is None:
                    raise CampoObrigatorioException("Produto associado ao lote não encontrado.")

                if produto_db.quantidade_disponivel < transacao.quantidade:
                    raise ValorInvalidoException("Quantidade de venda maior do que a disponível no produto.")

                if (produto_db.quantidade_disponivel + transacao.quantidade) <= produto_db.quantidade_minima:
                    self.emitir_alerta()

                lote_db.quantidade += transacao.quantidade
                db.commit()
                db.refresh(lote_db)

                produto_db.quantidade_disponivel += transacao.quantidade
                db.commit()
                db.refresh(produto_db)


            return {"quantidade":lote_db.quantidade}

        except CampoObrigatorioException as exc:
            db.rollback()
            raise HTTPException(status_code=400, detail=str(exc))
        except ValorInvalidoException as exc:
            db.rollback()
            raise HTTPException(status_code=400, detail=str(exc))

    def read_transacao(self, db: Session, transacao_id: int):
        try:
            transacao_db = db.query(TransacaoModel).filter(TransacaoModel.id == transacao_id).first()

            if transacao_db is None:
                raise CampoObrigatorioException("Transação não encontrada.")

            return self.transacao_view.format_response(transacao_db)
        except CampoObrigatorioException as exc:
            raise HTTPException(status_code=404, detail=str(exc))

    def emitir_alerta(self):
        print("| Produto: Camiseta branca | Codigo de barras: 111 11 1111 | Custo: R$ 45,50 | Preco de Venda: R$ 60,00 | Quantidade Atual: 5 | Fornecedor: Nike |")
