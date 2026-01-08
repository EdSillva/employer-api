import os
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()

def _int_from_env(var_name: str, default: int) -> int:
	try:
		return int(os.getenv(var_name, default))
	except (TypeError, ValueError):
		return default


def _bool_from_env(var_name: str, default: bool = False) -> bool:
	value = os.getenv(var_name)
	if value is None:
		return default

	return value.strip().lower() in {"1", "true", "t", "yes", "y", "on"}


SECRET_KEY = os.getenv(
	"SECRET_KEY",
	"09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7",
)
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = _int_from_env("ACCESS_TOKEN_EXPIRE_MINUTES", 30)
ACCESS_TOKEN_EXPIRE = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

SQL_ECHO = _bool_from_env("SQL_ECHO", False)
ENABLE_SEED = _bool_from_env("ENABLE_SEED", False)
