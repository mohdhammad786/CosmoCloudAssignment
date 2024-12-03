from pydantic import BaseModel
from typing import List
class Student(BaseModel):
    name: str
    age: int

class GetStudentListResponse(BaseModel):
    data: List[Student]
