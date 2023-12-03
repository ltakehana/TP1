import json
from app.models.filial_model import FilialModel
from app.models.fornecedor_model import FornecedorModel
from app.models.produto_model import ProdutoModel
from app.views.produto_view import ProdutoView
from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal, engine, Base

client = TestClient(app)


def setup_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    fornecedor = FornecedorModel(nome="Nome do Fornecedor")
    filialA = FilialModel(nome="Filial", endereco="Rua A",
                          telefone="(11)1111-1111")
    filialB = FilialModel(nome="FilialB", endereco="Rua B",
                          telefone="(22)2222-2222")
    produtoA = ProdutoModel(descricao="Produto Teste", codigo_barras="QWERTY",
                            custo=1.0, preco_venda=5.0, quantidade_disponivel=10, filial_id=1)
    produtoB = ProdutoModel(descricao="Produto Teste", codigo_barras="QWERTY",
                            custo=1.0, preco_venda=5.0, quantidade_disponivel=10, filial_id=2)

    db.add(fornecedor)
    db.add(filialA)
    db.add(filialB)
    db.add(produtoA)
    db.add(produtoB)

    db.commit()

    return db


def test_recebimento():
    db = setup_db()
    transacao_view = ProdutoView()

    transacao_data = {
        "quantidade": 5,
        "codigo_barras": "QWERTY",
        "fornecedor_id": 1,
        "filial_id": 1
    }

    produto = db.query(ProdutoModel).filter(
        ProdutoModel.codigo_barras == "QWERTY" and ProdutoModel.filial_id == 1).first()
    produto.quantidade_disponivel += 5

    response = client.post("/transacao/recebimento", json=transacao_data)

    assert response.status_code == 200
    assert response.json() == transacao_view.format_response(produto)

    db.close()


def test_ajuste():
    db = setup_db()
    transacao_view = ProdutoView()

    transacao_data = {
        "quantidade": 5,
        "codigo_barras": "QWERTY",
        "tipo": "ajustes",
        "filial_id": 1
    }

    produto = db.query(ProdutoModel).filter(
        ProdutoModel.codigo_barras == "QWERTY" and ProdutoModel.filial_id == 1).first()
    produto.quantidade_disponivel = 5

    response = client.post("/transacao", json=transacao_data)

    assert response.status_code == 200
    assert response.json() == transacao_view.format_response(produto)

    db.close()


def test_devolucao():
    db = setup_db()
    transacao_view = ProdutoView()

    transacao_data = {
        "quantidade": 5,
        "codigo_barras": "QWERTY",
        "tipo": "devolucao",
        "filial_id": 1
    }

    produto = db.query(ProdutoModel).filter(
        ProdutoModel.codigo_barras == "QWERTY" and ProdutoModel.filial_id == 1).first()
    produto.quantidade_disponivel += 5

    response = client.post("/transacao", json=transacao_data)

    assert response.status_code == 200
    assert response.json() == transacao_view.format_response(produto)

    db.close()


def test_venda():
    db = setup_db()
    transacao_view = ProdutoView()

    transacao_data = {
        "quantidade": 5,
        "codigo_barras": "QWERTY",
        "tipo": "venda",
        "filial_id": 1
    }

    produto = db.query(ProdutoModel).filter(
        ProdutoModel.codigo_barras == "QWERTY" and ProdutoModel.filial_id == 1).first()
    produto.quantidade_disponivel -= 5

    response = client.post("/transacao", json=transacao_data)

    assert response.status_code == 200
    assert response.json() == transacao_view.format_response(produto)

    db.close()


def test_transferencia():
    db = setup_db()
    transacao_view = ProdutoView()

    transacao_data = {
        "quantidade": 5,
        "codigo_barras": "QWERTY",
        "filial_origem": 1,
        "filial_destino": 2
    }

    produto_origem = db.query(ProdutoModel).filter(
        ProdutoModel.codigo_barras == "QWERTY" and ProdutoModel.filial_id == 1).first()
    produto_destino = db.query(ProdutoModel).filter(
        ProdutoModel.codigo_barras == "QWERTY" and ProdutoModel.filial_id == 2).first()

    produto_origem.quantidade_disponivel -= 5
    produto_destino.quantidade_disponivel += 5

    response = client.post("/transacao/transferencia", json=transacao_data)

    produtos = []
    produtos.append(produto_origem)
    produtos.append(produto_destino)

    assert response.status_code == 200
    assert response.json() == [transacao_view.format_response(
        produto_model) for produto_model in produtos]

    db.close()
