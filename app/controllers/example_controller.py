
from app.schemas.example_schema import ExampleSchema
from app.models.example_model import ExampleModel
from app.views.example_view import ExampleView
from sqlalchemy.orm import Session

class ExampleController:
    def __init__(self):
        self.example_view = ExampleView()

    def read_root(self, db: Session):
        example_data = db.query(ExampleModel).filter(ExampleModel.id == 1).first()

        if example_data:
            example_schema = ExampleSchema(**example_data.__dict__)
            return example_schema
        else:
            return {"message": "Example not found"}