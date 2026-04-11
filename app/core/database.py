from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

_engine = None
_session_factory = None


class Base(DeclarativeBase):
    pass


def get_engine():  # type: ignore[no-untyped-def]
    global _engine
    if _engine is None:
        if not settings.database_url:
            raise RuntimeError("DATABASE_URL not configured")
        _engine = create_async_engine(
            settings.database_url, echo=False, pool_size=10, max_overflow=20
        )
    return _engine


def get_session_factory():  # type: ignore[no-untyped-def]
    global _session_factory
    if _session_factory is None:
        _session_factory = async_sessionmaker(
            get_engine(), class_=AsyncSession, expire_on_commit=False
        )
    return _session_factory


async def get_db() -> AsyncSession:  # type: ignore[misc]
    factory = get_session_factory()
    async with factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
