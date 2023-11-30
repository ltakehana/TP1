from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine, SessionLocal

client = TestClient(app)

def setup_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    example_data = {"id": "1", "message": "Hello, World!"}
    db.add(ExampleModel(**example_data))
    db.commit()
    db.refresh(db)
    return db

def test_read_root():
    db = setup_db()

    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}

    db.close()
