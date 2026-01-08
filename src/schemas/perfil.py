from pydantic import BaseModel, EmailStr
from typing import Optional

from src.core.enums import Role

class PerfilBase(BaseModel):
    nome: str
    sobrenome: str
    usuario: str
    departamento: str
    email: EmailStr

class PerfilCreate(PerfilBase):
    password: str
    role: Role

class PerfilUpdate(BaseModel):
    nome: Optional[str] = None
    sobrenome: Optional[str] = None
    departamento: Optional[str] = None
    email: Optional[EmailStr] = None


class PerfilResponse(PerfilBase):
    id: int

    class Config:
        from_attributes = True
