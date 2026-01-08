from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.db.session import create_db_and_tables
from src.db.seed import create_seed_users
from src.routes.perfil import router as perfil_router
from src.routes.auth import router as auth_router
from src.db.session import engine
from sqlmodel import Session

from src.core.config import ENABLE_SEED

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()

    with Session(engine) as session:

        if ENABLE_SEED:
            create_seed_users(session)

    yield

app = FastAPI(
    title="CRUD Funcionários",
    lifespan=lifespan
)

app.include_router(auth_router)
app.include_router(perfil_router)
