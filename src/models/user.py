from sqlmodel import SQLModel, Field
from src.core.enums import Role


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)

    username: str = Field(unique=True, index=True)
    hashed_password: str

    role: Role
    departamento: str
    disabled: bool = False
