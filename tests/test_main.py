# tests/test_main.py
from fastapi.testclient import TestClient
from app.main import app
from app.models.example_model import ExampleModel
from app.database import SessionLocal, engine, Base

client = TestClient(app)

def setup_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    example_data = {"id": "1", "message": "Hello, World!"}
    example_model = ExampleModel(**example_data)
    
    db.add(example_model)
    db.commit()
    db.refresh(example_model)
    
    return db

def test_read_root():
    db = setup_db()

    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}

    db.close()
