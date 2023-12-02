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
        id = random.randint(1001, 1050),
        quantidade= 15,
        produto_id= produto.id,
        data_validade= "2023-12-11T00:44:07.446Z"
    )

    lote = LoteModel(**lote_data.dict())
    db.add(lote)
    db.commit()
    db.refresh(lote)


    return db, lote


def test_emitir_alerta_um():
    db, lote = setup_db()

    terminal = io.StringIO()
    sys.stdout = terminal

    body = {"quantidade": -10, "lote_id": lote.id}
    response = client.post("/transacao/ajuste/", json=body)

    sys.stdout = sys.__stdout__

    saida_terminal = terminal.getvalue()
    assert saida_terminal == "| Produto: Camiseta branca | Codigo de barras: 111 11 1111 | Custo: R$ 45,50 | Preco de Venda: R$ 60,00 | Quantidade Atual: 5 | Fornecedor: Nike |\n"

def test_emitir_alerta_dois():
    db, lote = setup_db()

    terminal = io.StringIO()
    sys.stdout = terminal

    body = {"quantidade": -11, "lote_id": lote.id}
    response = client.post("/transacao/ajuste/", json=body)

    sys.stdout = sys.__stdout__

    saida_terminal = terminal.getvalue()
    assert saida_terminal == "| Produto: Camiseta branca | Codigo de barras: 111 11 1111 | Custo: R$ 45,50 | Preco de Venda: R$ 60,00 | Quantidade Atual: 4 | Fornecedor: Nike |\n"
