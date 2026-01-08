from typing import Optional
from sqlmodel import SQLModel, Field

class Perfil(SQLModel, table=True):
    __tablename__ = "perfis"
    
    id: int | None = Field(default=None, primary_key=True)
    nome: str
    sobrenome: str
    usuario: str = Field(unique=True, index=True)
    email: str = Field(unique=True, index=True)
    departamento: str
    
    user_id: int = Field(foreign_key="users.id")