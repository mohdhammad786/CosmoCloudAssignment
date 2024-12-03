from typing import Optional
from pydantic import BaseModel, Field

class AddressUpdate(BaseModel):
    city: Optional[str] = Field(None, min_length=1, max_length=50)
    country: Optional[str] = Field(None, min_length=1, max_length=50)

class StudentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    age: Optional[int] = None
    address: Optional[AddressUpdate] = None
