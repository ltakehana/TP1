
from app.models.produto_model import ProdutoModel
from app.models.transacao_model import TransacaoModel, TransacaoRecebimentoModel, TransacaoTransferenciaModel
from app.schemas.transacao_schema import TransacaoRecebimentoSchema, TransacaoSchema, TransacaoTransferenciaSchema
from app.views.produto_view import ProdutoView
from sqlalchemy.orm import Session


class TransacaoController:
    def __init__(self):
        self.transacao_view = ProdutoView()

    def recebimento_produto(self, db: Session, transacao: TransacaoRecebimentoSchema):
        produto_db = db.query(ProdutoModel).filter(
            ProdutoModel.codigo_barras == transacao.codigo_barras and ProdutoModel.filial_id == transacao.filial_id).first()
        produto_db.quantidade_disponivel += transacao.quantidade

        transacao_db = TransacaoRecebimentoModel(quantidade=transacao.quantidade, produto_id=produto_db.id,
                                                 fornecedor_id=transacao.fornecedor_id, filial_id=transacao.filial_id)

        db.add(transacao_db)
        db.add(produto_db)
        db.commit()
        db.refresh(produto_db)

        return self.transacao_view.format_response(produto_db)

    def transacao_produto(self, db: Session, transacao: TransacaoSchema):
        if transacao.tipo == "ajustes":
            produto_db = db.query(ProdutoModel).filter(
                ProdutoModel.codigo_barras == transacao.codigo_barras and ProdutoModel.filial_id == transacao.filial_id).first()
            produto_db.quantidade_disponivel = transacao.quantidade
        elif transacao.tipo == "devolucao":
            produto_db = db.query(ProdutoModel).filter(
                ProdutoModel.codigo_barras == transacao.codigo_barras and ProdutoModel.filial_id == transacao.filial_id).first()
            produto_db.quantidade_disponivel += transacao.quantidade
        else:
            produto_db = db.query(ProdutoModel).filter(
                ProdutoModel.codigo_barras == transacao.codigo_barras and ProdutoModel.filial_id == transacao.filial_id).first()
            produto_db.quantidade_disponivel -= transacao.quantidade

        transacao_db = TransacaoModel(quantidade=transacao.quantidade, produto_id=produto_db.id,
                                      tipo=transacao.tipo, filial_id=transacao.filial_id)

        db.add(transacao_db)
        db.add(produto_db)
        db.commit()
        db.refresh(produto_db)

        return self.transacao_view.format_response(produto_db)

    def transferencia_produto(self, db: Session, transacao: TransacaoTransferenciaSchema):
        lista = []

        produtoA = db.query(ProdutoModel).filter(
            ProdutoModel.codigo_barras == transacao.codigo_barras and ProdutoModel.filial_id == transacao.filial_origem).first()
        produtoB = db.query(ProdutoModel).filter(
            ProdutoModel.codigo_barras == transacao.codigo_barras and ProdutoModel.filial_id == transacao.filial_destino).first()

        produtoA.quantidade_disponivel -= transacao.quantidade
        produtoB.quantidade_disponivel += transacao.quantidade

        transacao_db = TransacaoTransferenciaModel(quantidade=transacao.quantidade, produto_origem=produtoA.id,
                                                   produto_destino=produtoB.id, filial_origem=transacao.filial_origem, filial_destino=transacao.filial_destino)

        db.add(transacao_db)
        db.add(produtoA)
        db.add(produtoB)
        db.commit()
        db.refresh(produtoA)
        db.refresh(produtoB)

        lista.append(produtoA)
        lista.append(produtoB)

        lista_produtos_view = [self.transacao_view.format_response(
            produto_model) for produto_model in lista]

        return lista_produtos_view
