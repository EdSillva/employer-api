from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from src.db.session import get_session
from src.models.perfil import Perfil
from src.repositories.perfil_repository import (
    get_perfil_by_id,
    delete_perfil,
)
from src.repositories.perfil_repository import update_perfil
from src.core.dependencies import get_current_user
from src.models.user import User
from src.schemas.auth import UsuarioLogado
from src.schemas.perfil import PerfilCreate, PerfilResponse, PerfilUpdate
from src.services.perfil_service import (
    criar_usuario_e_perfil,
    listar_perfis, 
    validar_atualizacao, 
    validar_remocao
)

router = APIRouter(prefix="/perfis", tags=["Perfis"])

@router.post("/", response_model=PerfilResponse)
def criar(
    perfil: PerfilCreate,
    session: Session = Depends(get_session),
    current_user: UsuarioLogado = Depends(get_current_user),
):
    return criar_usuario_e_perfil(
        session=session,
        perfil=perfil,
        usuario_logado=current_user,
    )

@router.get("/", response_model=list[Perfil])
def listar(
    session: Session = Depends(get_session),
    current_user: UsuarioLogado = Depends(get_current_user),
    departamento: str | None = None,
    query: str | None = None,
):
    return listar_perfis(
        session=session,
        usuario=current_user,
        departamento=departamento,
        query=query,
    )


@router.put("/{perfil_id}", response_model=Perfil)
def atualizar(
    perfil_id: int,
    data: PerfilUpdate,
    session: Session = Depends(get_session),
    current_user: UsuarioLogado = Depends(get_current_user),
):
    perfil = get_perfil_by_id(session, perfil_id)

    validar_atualizacao(perfil, current_user)

    return update_perfil(session, perfil, data)

@router.delete("/{perfil_id}")
def deletar(
    perfil_id: int,
    session: Session = Depends(get_session),
    current_user: UsuarioLogado = Depends(get_current_user),
):
    perfil = get_perfil_by_id(session, perfil_id)

    validar_remocao(perfil, current_user)

    delete_perfil(session, perfil)
    return {"ok": True}


