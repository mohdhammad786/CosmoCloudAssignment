from fastapi import FastAPI
from pydantic import BaseModel,Field

class Address(BaseModel):
    city: str = Field(..., min_length=1, max_length=50)
    country: str = Field(..., min_length=1, max_length=50)

class Student(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    age: int
    address: Address 