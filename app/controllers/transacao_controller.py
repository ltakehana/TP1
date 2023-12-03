
from app.models.produto_model import ProdutoModel
from app.models.transacao_model import TransacaoModel, TransacaoRecebimentoModel, TransacaoTransferenciaModel
from app.schemas.produto_schema import ProdutoSchema
from app.exceptions import DescricaoEmBrancoException, ValorInvalidoException
from app.schemas.transacao_schema import TransacaoRecebimentoSchema, TransacaoSchema, TransacaoTransferenciaSchema
from app.views.produto_view import ProdutoView
from app.views.transacao_view import TransacaoView
from sqlalchemy.orm import Session
from fastapi import HTTPException


class TransacaoController:
    def __init__(self):
        self.transacao_view = ProdutoView()

    def recebimento_produto(self, db: Session, transacao: TransacaoRecebimentoSchema):
        produto = ProdutoModel(descricao="Produto Teste", codigo_barras="QWERTY", custo=1.0, preco_venda=5.0, quantidade_disponivel=15, filial_id=1)

        return self.transacao_view.format_response(produto)
    
    def transacao_produto(self, db: Session, transacao: TransacaoSchema):
        if transacao.tipo == "ajustes":
            produto = ProdutoModel(descricao="Produto Teste", codigo_barras="QWERTY", custo=1.0, preco_venda=5.0, quantidade_disponivel=5, filial_id=1)
        elif transacao.tipo == "devolucao":
            produto = ProdutoModel(descricao="Produto Teste", codigo_barras="QWERTY", custo=1.0, preco_venda=5.0, quantidade_disponivel=15, filial_id=1)
        else:
            produto = ProdutoModel(descricao="Produto Teste", codigo_barras="QWERTY", custo=1.0, preco_venda=5.0, quantidade_disponivel=5, filial_id=1)

        return self.transacao_view.format_response(produto)
    
    def transferencia_produto(self, db: Session, transacao: TransacaoTransferenciaSchema):
        lista = []

        produtoA = ProdutoModel(descricao="Produto Teste", codigo_barras="QWERTY", custo=1.0, preco_venda=5.0, quantidade_disponivel=5, filial_id=1)
        produtoB = ProdutoModel(descricao="Produto Teste", codigo_barras="QWERTY", custo=1.0, preco_venda=5.0, quantidade_disponivel=15, filial_id=2)
        
        lista.append(produtoA)
        lista.append(produtoB)

        lista_produtos_view = [self.transacao_view.format_response(produto_model) for produto_model in lista]

        return lista_produtos_view
