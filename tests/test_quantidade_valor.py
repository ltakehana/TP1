from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal, engine, Base
from app.schemas.produto_schema import ProdutoSchema
from app.models.produto_model import ProdutoModel

client = TestClient(app)

def setup_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    return db


def test_consultar_estoque():
    db = setup_db()
    
    produto = ProdutoSchema(
        codigo_barras= "111 000 000 11",
        custo= 100.00,
        descricao="Camisa Naruto",
        preco_venda= 120.00,
        quantidade_disponivel= 10
    )
    
    produto_db = ProdutoModel(**produto.dict())
    db.add(produto_db)
    db.commit()
    db.refresh(produto_db)

    response = client.get('coluna/' + str(produto_db.id) + '/')
    
    assert response.status_code == 200
    assert response.json() == {"quantidade": produto_db.quantidade_disponivel}
    
    db.close()
