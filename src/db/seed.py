from sqlmodel import Session, select

from src.models.user import User
from src.models.perfil import Perfil
from src.core.security import get_password_hash
from src.core.enums import Role


DEPARTAMENTOS = {
    "Financeiro": {
        Role.GESTOR: 1,
        Role.FUNCIONARIO: 3,
    },
    "Comercial": {
        Role.GESTOR: 1,
        Role.FUNCIONARIO: 3,
    },
    "TI": {
        Role.GESTOR: 1,
        Role.FUNCIONARIO: 3,
    },
}

def create_admin_user(session: Session):
    username = "admin"

    admin = session.exec(
        select(User).where(User.username == username)
    ).first()

    if admin:
        return admin

    admin = User(
        username=username,
        hashed_password=get_password_hash("admin123"),
        role=Role.SUPER,
        departamento="Admin",
    )

    session.add(admin)
    session.commit()
    session.refresh(admin)

    perfil = Perfil(
        nome="Admin",
        sobrenome="Sistema",
        usuario="admin",
        email="admin@empresa.com",
        departamento="Admin",
        user_id=admin.id,
    )

    session.add(perfil)
    session.commit()

    return admin


def create_seed_users(session: Session):
    create_admin_user(session)

    for departamento, cargos in DEPARTAMENTOS.items():
        for role, quantidade in cargos.items():
            for i in range(quantidade):
                username = f"{role.value}_{departamento.lower()}_{i+1}"

                user_exists = session.exec(
                    select(User).where(User.username == username)
                ).first()

                if user_exists:
                    continue

                user = User(
                    username=username,
                    hashed_password=get_password_hash("123456"),
                    role=role,
                    departamento=departamento,
                )

                session.add(user)
                session.commit()
                session.refresh(user)

                perfil = Perfil(
                    nome=role.value.capitalize(),
                    sobrenome=departamento,
                    usuario=username,
                    email=f"{username}@empresa.com",
                    departamento=departamento,
                    user_id=user.id,
                )

                session.add(perfil)
                session.commit()
