from fastapi import HTTPException
import pytest
from fastapi.testclient import TestClient
from app.exceptions import ValorIdNaoEncontrado
from app.main import app
from app.database import SessionLocal, engine, Base
from app.schemas.produto_schema import ProdutoSchema
from app.models.produto_model import ProdutoModel
from app.schemas.fornecedor_schema import FornecedorSchema
from app.models.fornecedor_model import FornecedorModel
from sqlalchemy.orm import Session

client = TestClient(app)


def setup_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    fornecedor_data = FornecedorSchema(
    nome= "Fornecedor A",
    endereco= "Rua A",
    telefone= "61 9 9999-9999"
    )

    fornecedor = FornecedorModel(**fornecedor_data.dict())
    db.add(fornecedor)
    db.commit()
    db.refresh(fornecedor)

    return db, fornecedor

def test_quantidade_valor_nao_encontrada():
    response = client.get('estoque/' + '10000' + '/')

    assert response.status_code == 400
    assert response.json() == {"detail":"Não foi encontrado nenhum seletor com tal id."}


@pytest.mark.parametrize("codigo_barras, descricao, quantidade_disponivel, search_key, expected_status, expected_json", [
    ("111 000 000 11", "Camisa Naruto", 10, "codigo_barras", 200, {"quantidade": 10}),
    ("111 000 000 10", "Camisa Sasuke", 15, "descricao", 200, {"quantidade": 15}),
    ("111 000 000 000", "", 10, "codigo_barras", 400, {"detail": "Descrição, código de barras, custo, preço de venda e quantidade disponível são obrigatórios."}),
])
def test_consultar_estoque(codigo_barras, descricao, quantidade_disponivel, search_key, expected_status, expected_json):
    db, fornecedor = setup_db()

    produto = ProdutoSchema(
        codigo_barras=codigo_barras,
        custo=100.00,
        descricao=descricao,
        preco_venda=120.00,
        quantidade_disponivel=quantidade_disponivel,
        fornecedor_id= fornecedor.id
    )

    produto_db = ProdutoModel(**produto.dict())
    db.add(produto_db)
    db.commit()
    db.refresh(produto_db)

    response = client.get(f'estoque/{codigo_barras if search_key == "codigo_barras"  else descricao}/')

    assert response.status_code == expected_status
    assert response.json() == expected_json

    db.close()
