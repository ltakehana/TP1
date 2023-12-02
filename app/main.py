from fastapi import FastAPI, Depends  
from sqlalchemy.orm import Session
from app.controllers.example_controller import ExampleController
from app.database import engine, SessionLocal, Base

app = FastAPI()
example_controller = ExampleController()

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
