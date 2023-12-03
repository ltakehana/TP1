from app.models.quantidade_valor_model import QuantidadeValorModel
from app.schemas.quantidade_valor_schema import QuantidadeValorSchema
from sqlalchemy.orm import Session
from fastapi import HTTPException

class RastreamentoController:

    def quantidade_total(db: Session, produto_id: int):      
        quantidade_total = db.query(func.sum(QuantidadeValorModel.quantidade)) \
            .filter(QuantidadeValorModel.produto_id == produto_id).scalar()
    
        if quantidade_total is None:
            quantidade_total = 0
        
        return quantidade_total
