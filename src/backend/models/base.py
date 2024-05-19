from datetime import datetime
from typing import List, Any, Tuple, Dict, Generator
import os

from dotenv import load_dotenv
from sqlalchemy.orm import DeclarativeBase, backref, relationship, declared_attr, Session, sessionmaker
from sqlalchemy import create_engine
from pydantic import BaseModel, Field
from backend.utils import timezone


load_dotenv()


id_key = Field(exclude=True, primary_key=True, description="Primary key identifier.")

"""
❓ MiXin https://github.com/tiangolo/sqlmodel/pull/256
"""

class UserMixin:
    create_user: int = Field(description="The user who created the record.")
    update_user: int | None = Field(exclude=True, default=None, description="The user who last updated the record.")
    delete_user: int | None = Field(exclude=True, default=None, description="The user who deleted the record.")
    

class TimestampMixin:
    created_time: datetime = Field(
        exclude=True,
        sa_column_kwargs={'default_factory': timezone.now},
        description="The time the record was created."
    )

    updated_time: datetime | None = Field(
        exclude=True,
        sa_column_kwargs={'onupdate': timezone.now},
        description="The time the record was last updated."
    )

    deleted_time: datetime | None = Field(
        exclude=True,
        default=None,
        description="The time the record was deleted."
    )

def query_data(self) -> str:
    return ', '.join(f'{k}={v}' for k, v in self.__dict__.items())

class BaseMixin(UserMixin, TimestampMixin):
    __tablename__: str
    id: int = id_key
    def __repr__(self) -> str: 
        return f"<{self.__class__.__name__} {query_data}>"
    

class Base(DeclarativeBase, BaseMixin):
    def __repr__(self) -> str: 
        return f"<{self.__class__.__name__} {query_data}>"
    
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()



def create_database(db_url: str) -> Session:
    engine = create_engine(os.getenv("N_DATABASE_URL"))
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()

def get_db() -> Generator[Session, None, None]:
    db = create_database(os.getenv("N_DATABASE_URL"))
    try:
        yield db
    finally:
        db.close()

        
    