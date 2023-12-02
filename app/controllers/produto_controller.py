
from app.models.produto_model import ProdutoModel
from app.schemas.produto_schema import ProdutoSchema
from app.views.produto_view import ProdutoView
from sqlalchemy.orm import Session

class ProdutoController:
    def __init__(self):
        self.produto_view = ProdutoView()

    def create_produto(self, db: Session, produto: ProdutoSchema):
        produto_db = ProdutoModel(**produto.dict())
        db.add(produto_db)
        db.commit()
        db.refresh(produto_db)
        return self.produto_view.format_response(produto_db)