from sqlalchemy import Column, String
from app.database import Base

class ExampleModel(Base):
    __tablename__ = "example_table"

    id = Column(String, primary_key=True, index=True)
    message = Column(String)
