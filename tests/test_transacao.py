from fastapi.testclient import TestClient
from app.main import app
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

from main import app, TransacaoSchema, TransacaoCreationSchema

client = TestClient(app)

@pytest.mark.parametrize("data, expected_status_code, expected_response", [
    ({"tipo": "venda", "quantidade": 10, "lote_id": 2022}, 200, {"quantidade": 12}),
])


def test_criar_transacao(data, expected_status_code, expected_response):
    response = client.post("/transacao/"+data.tipo, json=data)
    assert response.status_code == expected_status_code
    assert response.json() == expected_response
