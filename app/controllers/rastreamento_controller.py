from app.models.lote_model import LoteModel
from app.models.produto_model import ProdutoModel
from app.schemas.lote_schema import LoteSchema
from app.views.lote_view import LoteView
from app.exceptions import ValorIdNaoEncontrado, ValorInvalidoException
from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import func 

class RastreamentoController:
    def __init__(self):
        self.lote_view = LoteView()

    def create_lote(self, db: Session, lote: LoteSchema):
        try:            
            produto_existente = db.query(ProdutoModel).filter(ProdutoModel.id == lote.produto_id).first()

            if not produto_existente:
                raise HTTPException(status_code=400, detail="Produto não encontrado.")
            
            if lote.quantidade <=0:
                raise ValorInvalidoException()
            
            lote_db = LoteModel(**lote.dict())
            db.add(lote_db)
            db.commit()
            db.refresh(lote_db)
            
            return self.lote_view.format_response(lote_db)
        
        except ValorInvalidoException as exc:
            raise HTTPException(status_code=400, detail=str(exc))

    def quantidade_produto_lote(self, db: Session, lote_id: int): 
        try:     
            quantidade_total = db.query(func.sum(LoteModel.quantidade)) \
                .filter(LoteModel.id == lote_id).scalar()
                
            if quantidade_total is None:
                raise ValorIdNaoEncontrado()
            
            return {"quantidade": quantidade_total}
        
        except ValorIdNaoEncontrado as exc:
            raise HTTPException(status_code=400, detail=str(exc))
