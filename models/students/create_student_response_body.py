from pydantic import BaseModel

class CreateStudentResponseBody(BaseModel):
    id: str

