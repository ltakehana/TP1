from app.models.produto_model import ProdutoModel
from app.views.quantidade_valor import QuantidadeValorView
from app.exceptions import ValorIdNaoEncontrado, DescricaoEmBrancoException
from sqlalchemy.orm import Session
from fastapi import HTTPException

class QuantidadeValorController:
    def __init__(self):
        self.quantidade_valor_view = QuantidadeValorView()
        
    def quantidade_estoque(self, db: Session, produto_id):
        try:
            produto_db = db.query(ProdutoModel).filter(ProdutoModel.id == produto_id).first()
            
            if produto_db is None:
                raise ValorIdNaoEncontrado()

            return self.quantidade_valor_view.format_response(produto_db)
        except DescricaoEmBrancoException as exc:
            raise HTTPException(status_code=400, detail=str(exc))
                

    