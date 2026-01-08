from pydantic import BaseModel
from src.core.enums import Role

class Token(BaseModel):
    access_token: str
    token_type: str

class UsuarioLogado(BaseModel):
    id: int
    username: str
    role: Role
    departamento: str
