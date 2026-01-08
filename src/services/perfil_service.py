from fastapi import HTTPException, status
from sqlmodel import Session, select

from src.models.user import User
from src.models.perfil import Perfil
from src.repositories.perfil_repository import (
    list_perfis,
    list_perfis_by_departamento,
    search_perfis,
)
from src.schemas.perfil import PerfilCreate
from src.schemas.auth import UsuarioLogado
from src.core.security import get_password_hash
from src.core.enums import Role

def criar_usuario_e_perfil(
    session: Session,
    perfil: PerfilCreate,
    usuario_logado: UsuarioLogado,
):
    if usuario_logado.role == Role.FUNCIONARIO:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Funcionário não pode criar usuários"
        )

    if (
        usuario_logado.role == Role.GESTOR
        and perfil.departamento != usuario_logado.departamento
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Gestor só pode criar usuários do próprio departamento"
        )

    if session.exec(
        select(User).where(User.username == perfil.usuario)
    ).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username já existe"
        )

    if session.exec(
        select(Perfil).where(Perfil.email == perfil.email)
    ).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email já existe"
        )

    try:
        user = User(
            username=perfil.usuario,
            hashed_password=get_password_hash(perfil.password),
            role=perfil.role,
            departamento=perfil.departamento,
        )

        session.add(user)
        session.commit()
        session.refresh(user)

        perfil_db = Perfil(
            nome=perfil.nome,
            sobrenome=perfil.sobrenome,
            usuario=perfil.usuario,
            email=perfil.email,
            departamento=perfil.departamento,
            user_id=user.id,
        )

        session.add(perfil_db)
        session.commit()
        session.refresh(perfil_db)

        return perfil_db

    except HTTPException:
        raise
    except Exception:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao criar usuário e perfil"
        )

def listar_perfis(
    session: Session,
    usuario: UsuarioLogado,
    departamento: str | None = None,
    query: str | None = None,
):
    try:
        if usuario.role == Role.SUPER:
            if departamento or query:
                return search_perfis(session, departamento=departamento, query=query)
            return list_perfis(session)

        if usuario.role == Role.GESTOR:
            if query:
                return search_perfis(session, departamento=usuario.departamento, query=query)
            return list_perfis_by_departamento(session, usuario.departamento)

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Funcionário não pode listar perfis"
        )
    except HTTPException:
        raise
    except Exception:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao listar perfis"
        )
    
def validar_criacao_perfil(
    perfil: PerfilCreate,
    usuario: UsuarioLogado,
):
    try:
        if usuario.role == Role.FUNCIONARIO:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Funcionário não pode criar perfil"
            )

        if (
            usuario.role == Role.GESTOR
            and perfil.departamento != usuario.departamento
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Gestor só pode criar perfil do próprio departamento"
            )
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao validar criação de perfil"
        )


def validar_atualizacao(
    perfil: Perfil,
    usuario: UsuarioLogado,
):
    try:
        if not perfil:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Perfil não encontrado"
            )

        if usuario.role == Role.FUNCIONARIO:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Funcionário não pode atualizar perfil"
            )

        if (
            usuario.role == Role.GESTOR
            and perfil.departamento != usuario.departamento
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Gestor só pode atualizar perfis do seu departamento"
            )
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao validar atualização de perfil"
        )


def validar_remocao(
    perfil: Perfil,
    usuario: UsuarioLogado,
):
    try:
        if not perfil:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Perfil não encontrado"
            )

        if usuario.role == Role.FUNCIONARIO:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Funcionário não pode deletar perfil"
            )

        if (
            usuario.role == Role.GESTOR
            and perfil.departamento != usuario.departamento
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Gestor só pode deletar perfis do seu departamento"
            )
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao validar remoção de perfil"
        )
