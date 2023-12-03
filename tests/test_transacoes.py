import json
from app.models.filial_model import FilialModel
from app.models.fornecedor_model import FornecedorModel
from app.models.produto_model import ProdutoModel
from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal, engine, Base

client = TestClient(app)


def setup_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    return db


def test_recebimento():
    db = setup_db()

    transacao_data = {
        "quantidade": 5,
        "produto_id": 1,
        "fornecedor_id": 1,
        "filial_id": 1
    }

    produto = {
        "codigo_barras": "QWERTY",
        "descricao": "Produto Teste",
        "custo": 1.0,
        "preco_venda": 5.0,
        "quantidade_disponivel": 15,
        "filial_id": 1
    }

    response = client.post("/transacao/recebimento", json=transacao_data)

    assert response.status_code == 200
    assert response.json() == produto

    db.close()


def test_ajuste():
    db = setup_db()

    transacao_data = {
        "quantidade": 5,
        "produto_id": 1,
        "tipo": "ajustes",
        "filial_id": 1
    }

    produto = {
        "codigo_barras": "QWERTY",
        "descricao": "Produto Teste",
        "custo": 1.0,
        "preco_venda": 5.0,
        "quantidade_disponivel": 5,
        "filial_id": 1
    }

    response = client.post("/transacao", json=transacao_data)

    assert response.status_code == 200
    assert response.json() == produto

    db.close()


def test_devolucao():
    db = setup_db()

    transacao_data = {
        "quantidade": 5,
        "produto_id": 1,
        "tipo": "devolucao",
        "filial_id": 1
    }

    produto = {
        "codigo_barras": "QWERTY",
        "descricao": "Produto Teste",
        "custo": 1.0,
        "preco_venda": 5.0,
        "quantidade_disponivel": 15,
        "filial_id": 1
    }

    response = client.post("/transacao", json=transacao_data)

    assert response.status_code == 200
    assert response.json() == produto

    db.close()


def test_venda():
    db = setup_db()

    transacao_data = {
        "quantidade": 5,
        "produto_id": 1,
        "tipo": "venda",
        "filial_id": 1
    }

    produto = {
        "codigo_barras": "QWERTY",
        "descricao": "Produto Teste",
        "custo": 1.0,
        "preco_venda": 5.0,
        "quantidade_disponivel": 5,
        "filial_id": 1
    }

    response = client.post("/transacao", json=transacao_data)

    assert response.status_code == 200
    assert response.json() == produto

    db.close()


def test_transferencia():
    db = setup_db()

    transacao_data = {
        "quantidade": 5,
        "produto_id": 1,
        "filial_origem": 1,
        "filial_destino": 2
    }

    produtos = [
        {
            "codigo_barras": "QWERTY",
            "descricao": "Produto Teste",
            "custo": 1.0,
            "preco_venda": 5.0,
            "quantidade_disponivel": 5,
            "filial_id": 1
        },
        {
            "codigo_barras": "QWERTY",
            "descricao": "Produto Teste",
            "custo": 1.0,
            "preco_venda": 5.0,
            "quantidade_disponivel": 15,
            "filial_id": 2
        },
    ]

    response = client.post("/transacao/transferencia", json=transacao_data)

    assert response.status_code == 200
    assert response.json() == produtos

    db.close()
