from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session

from src.core.security import decode_token
from src.db.session import get_session
from src.repositories.user_repository import get_user_by_username
from src.schemas.auth import UsuarioLogado

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
) -> UsuarioLogado:
    payload = decode_token(token)
    username = payload.get("sub")

    if not username:
        raise HTTPException(status_code=401)

    user = get_user_by_username(session, username)
    if not user:
        raise HTTPException(status_code=401)

    return UsuarioLogado(
        id=user.id,
        username=user.username,
        role=user.role,
        departamento=user.departamento
    )
