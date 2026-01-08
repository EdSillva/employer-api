from fastapi import HTTPException, status
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from src.models.perfil import Perfil
from src.schemas.perfil import PerfilUpdate

def create_perfil(session: Session, perfil: Perfil) -> Perfil:
    session.add(perfil)
    session.commit()
    session.refresh(perfil)
    return perfil

def get_perfil_by_id(session: Session, perfil_id: int) -> Perfil | None:
    return session.get(Perfil, perfil_id)

def list_perfis(session: Session):
    return session.exec(select(Perfil)).all()


def list_perfis_by_departamento(session: Session, departamento: str):
    return session.exec(
        select(Perfil).where(Perfil.departamento == departamento)
    ).all()


def search_perfis(
    session: Session,
    *,
    query: str | None = None,
    departamento: str | None = None,
):
    statement = select(Perfil)

    if departamento:
        statement = statement.where(Perfil.departamento == departamento)

    if query:
        query = query.strip()

    if query:
        like = f"%{query}%"
        statement = statement.where(
            or_(
                Perfil.nome.ilike(like),
                Perfil.sobrenome.ilike(like),
                Perfil.usuario.ilike(like),
                Perfil.email.ilike(like),
                Perfil.departamento.ilike(like),
            )
        )

    return session.exec(statement).all()


def update_perfil(session: Session, perfil: Perfil, data: PerfilUpdate):
    updates = data.model_dump(exclude_unset=True, exclude_none=True)

    new_email = updates.get("email")
    if new_email is not None and new_email != perfil.email:
        email_exists = session.exec(
            select(Perfil).where(
                (Perfil.email == new_email) & (Perfil.id != perfil.id)
            )
        ).first()

        if email_exists:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email já existe",
            )

    for field, value in updates.items():
        setattr(perfil, field, value)

    try:
        session.add(perfil)
        session.commit()
        session.refresh(perfil)
        return perfil
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Violação de unicidade ao atualizar perfil",
        )
    except Exception:
        session.rollback()
        raise



def delete_perfil(session: Session, perfil: Perfil):
    session.delete(perfil)
    session.commit()
