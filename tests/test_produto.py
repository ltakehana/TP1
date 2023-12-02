from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal, engine, Base

client = TestClient(app)

def setup_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    return db

def test_cadastrar_produto():
    db = setup_db()

    produto_data = {
        "descricao": "Produto Teste",
        "codigo_barras": "123456789",
        "custo": 10.0,
        "preco_venda": 20.0,
        "quantidade_disponivel": 50
    }

    response = client.post("/produto/", json=produto_data)

    assert response.status_code == 200
    assert response.json() == produto_data

    db.close()


def test_cadastrar_produto_com_descricao_em_branco():
    db = setup_db()

    produto_data = {
        "descricao": "",  # Descrição em branco
        "codigo_barras": "123456789",
        "custo": 10.0,
        "preco_venda": 20.0,
        "quantidade_disponivel": 50
    }

    response = client.post("/produto/", json=produto_data)

    assert response.status_code == 400
    assert response.json() == {"detail":"Descrição, código de barras, custo, preço de venda e quantidade disponível são obrigatórios."}
    db.close()

def test_cadastrar_produto_com_valores_invalidos():
    db = setup_db()

    produto_data = {
        "descricao": "Produto Teste",
        "codigo_barras": "123456789",
        "custo": -5.0,  # Valor inválido
        "preco_venda": 0.0,  # Valor inválido
        "quantidade_disponivel": -10  # Valor inválido
    }

    response = client.post("/produto/", json=produto_data)

    assert response.status_code == 400
    assert response.json() == {"detail":"Custo, preço de venda e quantidade disponível devem ser maiores que zero."}


    db.close()