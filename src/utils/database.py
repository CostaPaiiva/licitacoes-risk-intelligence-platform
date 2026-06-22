import os

from dotenv import load_dotenv
from sqlalchemy import create_engine


load_dotenv()


def get_database_url() -> str:
    """
    Retorna a URL de conexão com o PostgreSQL.
    """
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        user = os.getenv("POSTGRES_USER", "admin")
        password = os.getenv("POSTGRES_PASSWORD", "admin")
        host = os.getenv("POSTGRES_HOST", "localhost")
        port = os.getenv("POSTGRES_PORT", "5432")
        database = os.getenv("POSTGRES_DB", "licitacoes_db")

        database_url = f"postgresql://{user}:{password}@{host}:{port}/{database}"

    return database_url


def get_engine():
    """
    Cria e retorna uma engine SQLAlchemy.
    """
    database_url = get_database_url()
    return create_engine(database_url)