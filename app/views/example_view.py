from app.schemas.example_schema import ExampleSchema

class ExampleView:
    @staticmethod
    def format_response(schema: ExampleSchema):
        return {"message": schema.message}
