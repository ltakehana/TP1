from fastapi import FastAPI, Depends  
from sqlalchemy.orm import Session
from app.controllers.example_controller import ExampleController
from app.controllers.produto_controller import ProdutoController
from app.controllers.rastreamento_controller import RastreamentoController
from app.schemas.produto_schema import ProdutoSchema
from app.schemas.quantidade_valor_schema import QuantidadeValorSchema
from app.database import engine, SessionLocal, Base

app = FastAPI()
example_controller = ExampleController()
produto_controller = ProdutoController()
rastreamento_controller = RastreamentoController()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root(db: Session = Depends(get_db)):
    return example_controller.read_root(db)

@app.post("/produto/", response_model=ProdutoSchema)
def create_produto(produto: ProdutoSchema, db: Session = Depends(get_db)):
    return produto_controller.create_produto(db, produto)


@app.get("/quantidade_total/{produto_id}", response_model=int)
 def quantidade_total(db: Session = Depends(get_db), quantidade: QuantidadeValorSchema):
    return rastreamento_controller.quantidade_total(db, quantidade)