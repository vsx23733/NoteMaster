from pydantic import BaseModel
from typing import Dict, Tuple
class Token(BaseModel):
    access_token: str
    token_type: str
    username: str
    email: str

class LoginRequest(BaseModel):
    username: str
    password: str

class User(BaseModel):
    username: str
    email: str

class SignupRequest(BaseModel):
    username: str
    email: str
    password: str

class EditAccountRequest(BaseModel):
    username: str
    email: str
    token: str

class DeleteAccountRequest(BaseModel):
    token: str


class QuestionRequest(BaseModel):
    note_title: str
    note_content: str

class StatModel(BaseModel):
    stats: Dict