from pydantic import BaseModel, EmailStr
from typing import Any, Optional

class PatientCreate(BaseModel):
    email: EmailStr

class PatientResponse(BaseModel):
    patient_id: str  # Changed from `int` to `str` to match the format

    class Config:
        from_attributes = True  # Updated for Pydantic v2

# Schema for login request body
class PatientLogin(BaseModel):
    patient_id: str  # The user logs in with their patient_id

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class Response(BaseModel):
    status: bool
    message: str
    data: Optional[Any] = {}  # Defaults to an empty object
