from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from src.db.session import get_session
from src.repositories.user_repository import authenticate_user
from src.core.security import create_access_token
from src.core.config import ACCESS_TOKEN_EXPIRE
from src.schemas.auth import Token
from src.core.enums import Role
from src.core.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])

def require_gestor_or_super(
    user = Depends(get_current_user),
):
    if user.role not in {Role.GESTOR, Role.SUPER}:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permissão insuficiente",
        )
    return user

@router.post("/token", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    user = authenticate_user(
        session,
        form_data.username,
        form_data.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha inválidos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token(
        data={"sub": user.username},
        expires=ACCESS_TOKEN_EXPIRE
    )

    return {"access_token": token, "token_type": "bearer"}
