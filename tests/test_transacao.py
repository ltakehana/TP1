import pytest
import random
from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal, engine, Base
from fastapi import HTTPException

from app.schemas.transacao_schema import TransacaoCreationSchema
from app.models.produto_model import ProdutoModel
from app.schemas.produto_schema import ProdutoSchema
from app.models.fornecedor_model import FornecedorModel
from app.schemas.fornecedor_schema import FornecedorSchema
from app.models.lote_model import LoteModel
from app.schemas.lote_schema import LoteSchema

client = TestClient(app)

def setup_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    fornecedor_data = FornecedorSchema(
    nome= "Adidas",
    endereco= "Rua A",
    telefone= "61 9 9999-9999"
    )

    fornecedor = FornecedorModel(**fornecedor_data.dict())
    db.add(fornecedor)
    db.commit()
    db.refresh(fornecedor)

    produto_data = ProdutoSchema(
        descricao= "Camiseta preta",
        codigo_barras= "111 11 1110",
        custo= 45.50,
        preco_venda= 60.0,
        quantidade_disponivel= 20,
        quantidade_minima = 5,
        fornecedor_id = fornecedor.id
    )

    produto = ProdutoModel(**produto_data.dict())
    db.add(produto)
    db.commit()
    db.refresh(produto)

    lote_data = LoteSchema(
        id= random.randint(0,1000),
        quantidade= 20,
        produto_id= produto.id,
        data_validade= "2023-12-11T00:44:07.446Z"
    )

    lote = LoteModel(**lote_data.dict())
    db.add(lote)
    db.commit()
    db.refresh(lote)

    return db, lote

@pytest.mark.parametrize("data_type, quantidade, expected_status_code, expected_response", [
    ("venda", 10, 200, {"quantidade": 10}),
    ("venda", 5, 200, {"quantidade": 15}),
    ("recebimento", 13, 200, {"quantidade": 33}),
    ("devolucao", 1, 200, {"quantidade": 21}),
    ("transferencia", 10, 200, {"quantidade": 10}),
    ("ajuste", 10, 200, {"quantidade": 30}),
    ("ajuste", -1, 200, {"quantidade": 19})
])

def test_criar_transacao(data_type, quantidade, expected_status_code, expected_response):
    db, lote = setup_db()

    data = {"quantidade": quantidade, "lote_id":lote.id}
    response = client.post("/transacao/"+data_type+"/", json=data)

    assert response.status_code == expected_status_code
    assert response.json() == expected_response

    db.close()
