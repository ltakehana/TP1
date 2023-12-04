from fastapi.testclient import TestClient
from main import app
from app.database import SessionLocal, engine, Base
from app.views.transacao_view import TransacaoView
from app.schemas.transacao_schema import TransacaoSchema,TransacaoCreationSchema 
from app.models.transacao_model import TransacaoModel     
import pytest

client = TestClient(app)


def setup_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    return db


client = TestClient(app)

@pytest.mark.parametrize("data_type, data, expected_status_code, expected_response", [
    ("venda", {"quantidade": 10, "lote_id": 2022}, 200, {"quantidade": 12}),
    ("venda", {"quantidade": 5, "lote_id": 2022}, 200, {"quantidade": 7}), 
    ("recebimento", {"quantidade": 13, "lote_id": 2022}, 200, {"quantidade": 20}), 
    ("devolucao", {"quantidade": 1, "lote_id": 2022}, 200, {"quantidade": 21}), 
    ("transferencia", {"quantidade": 10, "lote_id": 2022}, 200, {"quantidade": 11}), 
    ("ajuste", {"quantidade": 10, "lote_id": 2022}, 200, {"quantidade": 21}), 
    ("ajuste", {"quantidade": -1, "lote_id": 2022}, 200, {"quantidade": 20})
])


def test_criar_transacao(data_type, data, expected_status_code, expected_response):
    print("/transacao/"+data_type+"/")
    response = client.post("/transacao/"+data_type+"/", json=data)
    assert response.status_code == expected_status_code
    assert response.json() == expected_response

