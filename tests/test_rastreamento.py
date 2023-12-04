from fastapi.testclient import TestClient
from datetime import datetime, timezone
from app.main import app
from app.database import SessionLocal, engine, Base
from app.schemas.lote_schema import LoteSchema
from fastapi import HTTPException
import pytest
from app.models.lote_model import LoteModel
from sqlalchemy.orm import Session

client = TestClient(app)

def setup_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    return db

def test_cadastrar_lote1():
    db = setup_db()
    
    # produto_data = {
    #     "descricao": "Shampoo", 
    #     "codigo_barras": "12345",
    #     "custo": 10.0,
    #     "preco_venda": 20.0,
    #     "quantidade_disponivel": 50
    # }
    lote_data = {
        "id": 2121,
        "quantidade": 10,
        "produto_id": 1,
        "data_validade": "2023-12-11T00:44:07.446Z"
    }
    
    response = client.post("/lote/", json=lote_data)

    assert response.status_code == 200
    assert response.json() == lote_data

    db.close()
    
def test_cadastrar_lote2():
    db = setup_db()
    
    # produto_data = {
    #     "descricao": "Shampoo", 
    #     "codigo_barras": "12345",
    #     "custo": 10.0,
    #     "preco_venda": 20.0,
    #     "quantidade_disponivel": 50
    # }
    lote_data = {
        "id": 2020,
        "quantidade": 22,
        "produto_id": 1,
        "data_validade": "2024-05-12T00:44:07.446Z"
    }
    
    response = client.post("/lote/", json=lote_data)

    assert response.status_code == 200
    assert response.json() == lote_data

    db.close()
     
def test_lote_nao_encontrada():
    response = client.get('lote/' + '10999' + '/')
    
    assert response.status_code == 400
    assert response.json() == {"detail":"Não foi encontrado nenhum seletor com tal id."}

def test_quantidade_produto_lote():   
    db = setup_db()
    
    lote = LoteSchema(
        id = 2222,
        quantidade = 10,
        produto_id = 1,
        data_validade = "2023-12-11T00:44:07.446Z"
    )
    
    lote_db = LoteModel(**lote.dict())
    db.add(lote_db)
    db.commit()
    db.refresh(lote_db)
    
    response = client.get('lote/' + str(lote.id) + '/')
    
    assert response.status_code == 200
    assert response.json() == {"quantidade": lote.quantidade}
    
    db.close()
