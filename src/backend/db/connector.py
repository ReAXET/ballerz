"""Works as of 5-13-2024 0445 CST"""
"""Main SQLAlchemy connector module. Contains the database connection and session management along with the base model class."""
import sys

from typing import Any, Dict, List, Optional, Annotated
from uuid import uuid4, UUID

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from sqlalchemy import URL, create_engine, Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from loguru import logger
from backend.core.config import settings

def create_async_engine_and_session(url: str | URL):
    try:
        engine_async = create_async_engine(url, echo=settings.DB_ECHO, future=True, pool_pre_ping=True)
        logger.info("Database connection established.")
    except Exception as e:
        logger.error(f"❌ Database connection error: {e}")
        sys.exit(1)

    else:
        db_async_session = async_sessionmaker(bind=engine_async, autoflush=False, expire_on_commit=False)
        return engine_async, db_async_session
    

def create_engine_and_session(url: str | URL):
    try:
        engine = create_engine(url, echo=settings.DB_ECHO, pool_pre_ping=True)
        logger.info("Database connection established.")
    except Exception as e:
        logger.error(f"❌ Database connection error: {e}")
        sys.exit(1)

    else:
        db_session = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
        return engine, db_session
    

ASYNC_DB_URL = (
    f"postgresql+asyncpg://{settings.NEON_USERNAME}:{settings.NEON_PASSWORD}@{settings.NEON_HOSTNAME}:{settings.NEON_PORT}/{settings.NEON_DB_NAME}"                                                                 
)
    

DB_URL = (
    f"postgresql+psycopg2://{settings.LOCAL_DB_USERNAME}:{settings.LOCAL_DB_PASSWORD}@{settings.LOCAL_DB_HOSTNAME}:{settings.LOCAL_DB_PORT}/{settings.LOCAL_DB_NAME}"
)

async_engine, async_db_session = create_async_engine_and_session(ASYNC_DB_URL)
engine, db_session = create_engine_and_session(DB_URL)

async def get_async_db() -> AsyncSession: # type: ignore
    async_db = async_db_session()
    try:
        yield async_db
    except Exception as e:
        logger.error(f"❌ Database error: {e}") 
        await async_db.rollback()
        raise e
    finally:
        await async_db.close()

    
def get_db() -> Session: # type: ignore
    db = db_session()
    try:
        yield db
    except Exception as e:
        logger.error(f"❌ Database error: {e}")
        db.rollback()
        raise e
    finally:
        db.close()


# Session Annotation
CurrentSession = Annotated[Session, AsyncSession, Depends(get_db), Depends(get_async_db)]

async def create_all_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(DeclarativeBase.metadata.create_all)


def create_all_tables_sync():
    with engine.begin() as conn:
        conn.run_sync(DeclarativeBase.metadata.create_all)


def uuid4_str() -> str:
    return str(uuid4())



############################################################################################################
#                                      Everything Works above this line                                    #
############################################################################################################

