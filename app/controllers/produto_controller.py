
from app.models.produto_model import ProdutoModel
from app.models.lote_model import LoteModel
from app.schemas.produto_schema import ProdutoSchema,ProdutoCreationSchema
from app.schemas.lote_schema import LoteSchema
from app.views.produto_view import ProdutoView
from app.exceptions import DescricaoEmBrancoException,ValorInvalidoException,ValorIdNaoEncontrado,FaltaLoteException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi import HTTPException


class ProdutoController:
    def __init__(self):
        self.produto_view = ProdutoView()

    def create_produto(self, db: Session, produto: ProdutoCreationSchema):
        try:
            if produto.custo <=0 or produto.preco_venda <=0 or produto.quantidade_disponivel<=0:
                raise ValorInvalidoException()
            if not produto.descricao or produto.descricao == "" or not produto.codigo_barras or produto.codigo_barras == "" or not produto.custo or not produto.preco_venda or not produto.quantidade_disponivel:
                raise DescricaoEmBrancoException()

            if not produto.lote or not produto.validade:
                raise FaltaLoteException()

            produto_schema = ProdutoSchema(
                codigo_barras= produto.codigo_barras,
                custo=  produto.custo,
                descricao=produto.descricao,
                preco_venda= produto.preco_venda,
                quantidade_disponivel= produto.quantidade_disponivel,
                fornecedor_id= produto.fornecedor_id
            )

            produto_db = ProdutoModel(**produto_schema.dict())
            db.add(produto_db)
            db.commit()
            db.refresh(produto_db)


            lote_data = LoteSchema(
                id= produto.lote,
                quantidade= produto_db.quantidade_disponivel,
                produto_id= produto_db.id,
                data_validade= produto.validade
            )

            lote_db=LoteModel(**lote_data.dict())

            db.add(lote_db)
            db.commit()
            db.refresh(lote_db)

            return self.produto_view.format_response(produto_db)
        except DescricaoEmBrancoException as exc:
            raise HTTPException(status_code=400, detail=str(exc))
        except ValorInvalidoException as exc:
            raise HTTPException(status_code=400, detail=str(exc))
        except FaltaLoteException as exc:
            raise HTTPException(status_code=400, detail=str(exc))


    def read_produto(self, db: Session, produto):
        try:
            produto_db = db.query(ProdutoModel).filter(
                or_(
                    ProdutoModel.descricao == produto,
                    ProdutoModel.codigo_barras == produto
                )
            ).first()

            if produto_db is None:
                raise ValorIdNaoEncontrado()
            if not produto_db.descricao or produto_db.descricao == "":
                raise DescricaoEmBrancoException()

            return self.produto_view.format_response(produto_db)
        except DescricaoEmBrancoException as exc:
            raise HTTPException(status_code=400, detail=str(exc))
        except ValorIdNaoEncontrado as exc:
            raise HTTPException(status_code=400, detail=str(exc))
