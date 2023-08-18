from fastapi import Depends
from sqlmodel import SQLModel, create_engine, Session
from typing import Annotated

from config import settings


engine = create_engine(settings.POSTGRES_URL)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_db():
    with Session(engine) as session:
        yield session

Database = Annotated[Session, Depends(get_db)]