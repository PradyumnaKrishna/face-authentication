from sqlmodel import SQLModel, create_engine, Session

from .settings import get_settings

engine = create_engine(get_settings().SQLDB_URI)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
