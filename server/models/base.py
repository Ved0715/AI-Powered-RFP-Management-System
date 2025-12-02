from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
import enum
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://rfp_user:rfp_password@localhost:5432/rfp_db"
)

engine = create_async_engine(
    DATABASE_URL,
    echo=True, 
    future=True,
    pool_pre_ping=True,  
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

Base = declarative_base()


async def get_db():
    """
    Database session dependency for FastAPI.
    Usage in routes: db: AsyncSession = Depends(get_db)
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


class RFPStatus(str, enum.Enum):
    """RFP processing status"""
    NEW = "NEW"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class ProposalStatus(str, enum.Enum):
    """Proposal status"""
    DRAFT = "DRAFT"
    GENERATED = "GENERATED"
    SENT = "SENT"


async def init_db():
    """Create all tables in database"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_db():
    """Drop all tables in database"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)