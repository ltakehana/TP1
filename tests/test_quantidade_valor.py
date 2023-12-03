from fastapi import HTTPException
import pytest
from fastapi.testclient import TestClient
from app.exceptions import ValorIdNaoEncontrado
from app.main import app
from app.database import SessionLocal, engine, Base
from app.schemas.produto_schema import ProdutoSchema
from app.models.produto_model import ProdutoModel
from sqlalchemy.orm import Session

client = TestClient(app)


def setup_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    return db


def test_consultar_estoque():
    db = setup_db()
    
    produto = ProdutoSchema(
        codigo_barras= "111 000 000 11",
        custo= 100.00,
        descricao="Camisa Naruto",
        preco_venda= 120.00,
        quantidade_disponivel= 10,
        filial_id=1
    )
    
    produto_db = ProdutoModel(**produto.dict())
    db.add(produto_db)
    db.commit()
    db.refresh(produto_db)

    response = client.get('estoque/' + produto_db.codigo_barras + '/')
    
    assert response.status_code == 200
    assert response.json() == {"quantidade": produto_db.quantidade_disponivel}
    
    db.close()
    
def test_consultar_estoque_descricao():
    db = setup_db()
    
    produto = ProdutoSchema(
        codigo_barras= "111 000 000 10",
        custo= 100.00,
        descricao="Camisa Sasuke",
        preco_venda= 120.00,
        quantidade_disponivel= 15,
        filial_id=1
    )
    
    produto_db = ProdutoModel(**produto.dict())
    db.add(produto_db)
    db.commit()
    db.refresh(produto_db)

    response = client.get('estoque/' + produto_db.descricao + '/')
    
    assert response.status_code == 200
    assert response.json() == {"quantidade": produto_db.quantidade_disponivel}
    
    db.close()

def test_quantidade_valor_nao_encontrada():
    response = client.get('estoque/' + '10000' + '/')
    
    assert response.status_code == 400
    assert response.json() == {"detail":"Não foi encontrado nenhum seletor com tal id."}

def test_consultar_estoque_com_descricao_em_branco():
    
    db = setup_db()
    
    produto = ProdutoSchema(
        codigo_barras= "111 000 000 000",
        custo= 100.00,
        descricao="",
        preco_venda= 120.00,
        quantidade_disponivel= 10,
        filial_id=1
    )
    
    produto_db = ProdutoModel(**produto.dict())
    db.add(produto_db)
    db.commit()
    db.refresh(produto_db)

    response = client.get('estoque/' + produto_db.codigo_barras + '/')
    print(response)
    assert response.status_code == 400
    assert response.json() == {"detail":"Descrição, código de barras, custo, preço de venda e quantidade disponível são obrigatórios."}
    