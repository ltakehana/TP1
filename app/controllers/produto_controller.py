
from app.models.produto_model import ProdutoModel
from app.schemas.produto_schema import ProdutoSchema
from app.views.produto_view import ProdutoView
from app.exceptions import DescricaoEmBrancoException,ValorInvalidoException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi import HTTPException


class ProdutoController:
    def __init__(self):
        self.produto_view = ProdutoView()

    def create_produto(self, db: Session, produto: ProdutoSchema):
        try:
            if produto.custo <=0 or produto.preco_venda <=0 or produto.quantidade_disponivel<=0:
                raise ValorInvalidoException()
            if not produto.descricao or produto.descricao == "" or not produto.codigo_barras or produto.codigo_barras == "" or not produto.custo or not produto.preco_venda or not produto.quantidade_disponivel:
                raise DescricaoEmBrancoException()
            
            produto_db = ProdutoModel(**produto.dict())
            db.add(produto_db)
            db.commit()
            db.refresh(produto_db)
            return self.produto_view.format_response(produto_db)
        except DescricaoEmBrancoException as exc:
            raise HTTPException(status_code=400, detail=str(exc))
        except ValorInvalidoException as exc:
            raise HTTPException(status_code=400, detail=str(exc))


    def read_produto(self, db: Session, produto):
        produto_db = db.query(ProdutoModel).filter(
            or_(
                ProdutoModel.descricao == produto,
                ProdutoModel.codigo_barras == produto
            )
        ).first()
        return self.produto_view.format_response(produto_db)