from sqlmodel import Session, select
from src.models.user import User
from src.core.security import verify_password

def get_user_by_username(
    session: Session,
    username: str
) -> User | None:
    statement = select(User).where(User.username == username)
    return session.exec(statement).first()

def authenticate_user(
    session: Session,
    username: str,
    password: str
) -> User | None:
    user = get_user_by_username(session, username)
    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    if user.disabled:
        return None

    return user
