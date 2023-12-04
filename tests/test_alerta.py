import pytest
import random
import io
import sys
from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal, engine, Base

from unittest import TestCase
from app.models.produto_model import ProdutoModel
from app.schemas.produto_schema import ProdutoSchema
from app.models.fornecedor_model import FornecedorModel
from app.schemas.fornecedor_schema import FornecedorSchema
from app.models.lote_model import LoteModel
from app.schemas.lote_schema import LoteSchema
from app.exceptions import EstoqueNegativoException

client = TestClient(app)

def setup_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    fornecedor_data = FornecedorSchema(
    nome= "Nike",
    endereco= "Rua A",
    telefone= "61 9 9999-9999"
    )

    fornecedor = FornecedorModel(**fornecedor_data.dict())
    db.add(fornecedor)
    db.commit()
    db.refresh(fornecedor)

    produto_data = ProdutoSchema(
        descricao= "Camiseta branca",
        codigo_barras= "111 11 1111",
        custo= 45.50,
        preco_venda= 60.0,
        quantidade_disponivel= 15,
        quantidade_minima = 5,
        fornecedor_id = fornecedor.id
    )

    produto = ProdutoModel(**produto_data.dict())
    db.add(produto)
    db.commit()
    db.refresh(produto)

    lote_data = LoteSchema(
        id = random.randint(1001, 1500),
        quantidade= 15,
        produto_id= produto.id,
        data_validade= "2023-12-11T00:44:07.446Z"
    )

    lote = LoteModel(**lote_data.dict())
    db.add(lote)
    db.commit()
    db.refresh(lote)


    return db, lote

@pytest.mark.parametrize("quantidade_ajuste, quantidade_final", [
    (-10, 5),
    (-11, 4),
    (-12, 3)
])
def test_emitir_alerta(quantidade_ajuste, quantidade_final):
    db, lote = setup_db()

    terminal = io.StringIO()
    sys.stdout = terminal

    body = {"quantidade": quantidade_ajuste, "lote_id": lote.id}
    response = client.post("/transacao/ajuste/", json=body)

    sys.stdout = sys.__stdout__

    saida_terminal = terminal.getvalue()
    assert saida_terminal == f"| Produto: Camiseta branca | Codigo de barras: 111 11 1111 | Custo: R$ 45,50 | Preco de Venda: R$ 60,00 | Quantidade Atual: {quantidade_final} | Fornecedor: Nike |\n"

def teste_disparar_excecao():
    db, lote = setup_db()

    with pytest.raises(EstoqueNegativoException):

        body = {"quantidade": -50, "lote_id": lote.id}
        response = client.post("/transacao/ajuste/", json=body)

        assert response.status_code == 400
