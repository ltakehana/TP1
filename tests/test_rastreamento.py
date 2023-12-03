from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal, engine, Base

client = TestClient(app)

def setup_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    return db


def test_get_quantidade_total():
    db = setup_db()

    produto_id = 1
    quantidade_valor = QuantidadeValorModel(produto_id=produto_id, quantidade=5, valor_total=50.0)
    db.add(quantidade_valor)
    db.commit()

    response = client.get(f"/quantidade_total/{produto_id}")
    assert response.status_code == 200
    assert response.json() == 5 

    response = client.get("/quantidade_total/2")
    assert response.status_code == 200
    assert response.json() == 0 
