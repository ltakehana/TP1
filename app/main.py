from fastapi import FastAPI, Depends  
from sqlalchemy.orm import Session
from app.controllers.produto_controller import ProdutoController
from app.controllers.rastreamento_controller import RastreamentoController
from app.controllers.quantidade_valor_controller import QuantidadeValorController
from app.schemas.produto_schema import ProdutoSchema,ProdutoCreationSchema
from app.schemas.lote_schema import LoteSchema
from app.database import engine, SessionLocal, Base

app = FastAPI()
produto_controller = ProdutoController()
rastreamento_controller = RastreamentoController()
quantidade_valor_controller = QuantidadeValorController()

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
def read_root():
    return {"message":"Hello World!"}

@app.post("/produto/", response_model=ProdutoSchema)
def create_produto(produto: ProdutoCreationSchema, db: Session = Depends(get_db)):
    return produto_controller.create_produto(db, produto)

@app.post("/lote/", response_model=LoteSchema)
def create_lote(lote: LoteSchema, db: Session = Depends(get_db)):
    return rastreamento_controller.create_lote(db, lote)

@app.get("/lote/{lote_id}")
def quantidade_produto_lote(lote_id: int, db: Session = Depends(get_db)):
    return rastreamento_controller.quantidade_produto_lote(db, lote_id)

@app.get("/produto/{produto}/", response_model=ProdutoSchema)
def read_produto(produto: str, db: Session = Depends(get_db)):
    return produto_controller.read_produto(db, produto)


@app.get("/estoque/{produto}/")
def contar_estoque(produto: str, db: Session = Depends(get_db)):
    return quantidade_valor_controller.quantidade_estoque(db, produto)
