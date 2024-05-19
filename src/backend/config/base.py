from __future__ import annotations

import binascii 
import json
import os
from dataclasses import dataclass, field
from functools import lru_cache
from typing import TYPE_CHECKING, Any, Final
from pathlib import Path

from litestar.serialization import decode_json, encode_json
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine
from sqlalchemy.pool import NullPool
from redis.asyncio import Redis

from backend.utils.utilities import module_to_os_path, slugify



if TYPE_CHECKING:
    from litestar.data_extractors import RequestExtractorField, ResponseExtractorField


DEFAULT_MODULE_NAME = "backend"
BASE_DIR: Final[Path] = module_to_os_path(DEFAULT_MODULE_NAME)


TRUE_VALUES = {"True", "true", "1", "yes", "Yes", "YES", "on", "On", "ON", "T", "t"}



@dataclass
class DatabaseSettings:
    ECHO: bool = field(
        default_factory=lambda: os.getenv("DATABASE_ECHO", "False") in {"True", "true", "1", "yes", "Yes", "YES", "on", "On", "ON", "T", "t", "debug", "Debug", "DEBUG"},
        metadata={"description": "Echo SQL queries to the console"},
    )

    ECHO_POOL: bool = field(
        default_factory=lambda: os.getenv("DATABASE_ECHO_POOL", "False") in {"True", "true", "1", "yes", "Yes", "YES", "on", "On", "ON", "T", "t", "debug", "Debug", "DEBUG"},
        metadata={"description": "Echo connection pool events to the console"},
    )

    POOL_DISABLED: bool = field(
        default_factory=lambda: os.getenv("DATABASE_POOL_DISABLED", "False") in TRUE_VALUES,
        metadata={"description": "Disable connection pooling"},
    )

    POOL_MAX_OVERFLOW: int = field(
        default_factory=lambda: int(os.getenv("DATABASE_POOL_MAX_OVERFLOW", 10)),
        metadata={"description": "The maximum overflow size of the pool"},
    )

    POOL_SIZE: int = field(
        default_factory=lambda: int(os.getenv("DATABASE_POOL_SIZE", 5)),
        metadata={"description": "The number of connections to keep open inside the connection pool"},
    )

    POOL_TIMEOUT: int = field(
        default_factory=lambda: int(os.getenv("DATABASE_POOL_TIMEOUT", 30)),
        metadata={"description": "The number of seconds to wait before giving up on getting a connection from the pool"},
    )

    POOL_RECYCLE: int = field(
        default_factory=lambda: int(os.getenv("DATABASE_POOL_RECYCLE", 3600)),
        metadata={"description": "The number of seconds after which a connection is automatically recycled"},
    )

    POOL_PRE_PING: bool = field(
        default_factory=lambda: os.getenv("DATABASE_POOL_PRE_PING", "False") in TRUE_VALUES,
        metadata={"description": "Pre-ping connections to check if they are alive"},
    )

    URL: str = field(
        default_factory=lambda: os.getenv("DATABASE_URL", ""),
        metadata={"description": "The database URL"},
    )

    MIGRATION_CONFIG: str = f"{BASE_DIR}/db/migrations/alembic.ini"

    MIGRATION_PATH: str = f"{BASE_DIR}/db/migrations"

    MIGRATION_DDL_VERSION_TABLE: str = "ddl_version"

    FIXTURE_PATH: str = f"{BASE_DIR}/db/fixtures"

    _engine_instance: AsyncEngine | None = None

    @property
    def engine(self) -> AsyncEngine:
        return self.get_engine()
    

    def get_engine(self) -> AsyncEngine:
        if self._engine_instance is not None:
            return self._engine_instance
        
        if self.URL.startswith("postgresql+asyncpg"):
            self._engine_instance = create_async_engine(
                url = self.URL,
                future=True,
                json_serializer=encode_json,
                json_deserializer=decode_json,
                echo=self.ECHO,
                echo_pool=self.ECHO_POOL,
                max_overflow=self.POOL_MAX_OVERFLOW,
                pool_size=self.POOL_SIZE,
                pool_timeout=self.POOL_TIMEOUT,
                pool_recycle=self.POOL_RECYCLE,
                pool_pre_ping=self.POOL_PRE_PING,
                pool_use_lifo=True,
                poolclass=NullPool if self.POOL_DISABLED else None,
            )                                                                               
            """Database session factory
            see ['async_sessionmaker'](https://docs.sqlalchemy.org/en/14/orm/session_api.html#sqlalchemy.orm.session.async_sessionmaker)
            """

    @event.listens_for(engine.sync_engine, "before_cursor_execute")
    def _sqla_on_connect(dbapi_connection: Any, _: Any) -> Any:

        def encoder(bin_value: bytes) -> bytes:
            return b"\x01" + encode_json(bin_value)
        
        def decoder(bin_value: bytes) -> Any:
            # the byte is the \x01 prefix for jsonb used in postgres
            # asyncpg returns it when format='binary'
            return decode_json(bin_value[1:])
        
        dbapi_connection.await_(
            dbapi_connection.driver_connection.set_type_codec(
                "jsonb",
                encoder=encoder,
                decoder=decoder,
                schema="pg_catalog",
                format="binary",
            ),
        )
        dbapi_connection.await_(
            dbapi_connection.driver_connection.set_type_codec(
                "json",
                encoder=encoder,
                decoder=decoder,
                schema="pg_catalog",
                format="binary",
            ),
        )

    



