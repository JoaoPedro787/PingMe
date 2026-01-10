from fastapi import Depends
from typing import Annotated
from sqlmodel import create_engine, SQLModel, Session

engine = create_engine(
    "postgresql://postgres:root@localhost:5432/onlinechat", echo=True
)


# Apenas no startup da api
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


# Importo em todas as sessões de rota
SessionDep = Annotated[Session, Depends(get_session)]
