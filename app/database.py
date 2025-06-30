# database.py

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import os
import dotenv
from sqlalchemy import create_engine


# Load environment variables from .env file
dotenv.load_dotenv()

# Fetch the DATABASE_URL from the environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in the .env file.")

# Create the async engine using asyncpg
engine = create_async_engine(DATABASE_URL, echo=True)

# Create the session maker for async sessions
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Sync engine (used in scripts like seeder.py)
SYNC_DATABASE_URL = DATABASE_URL.replace("asyncmy", "pymysql")  # or "asyncpg" → "psycopg2" for Postgres
sync_engine = create_engine(SYNC_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=sync_engine)

# Base class for models to inherit from
from sqlalchemy.ext.declarative import declarative_base,DeclarativeMeta
Base:DeclarativeMeta = declarative_base()

# Initialize the database by creating tables
from app import models
async def init_db():
    """Create the database tables if they don't exist."""
    # from .models import models  # Import all models to ensure they are registered
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)  # Create tables in the database

# Dependency to get the database session for FastAPI routes
async def get_db():
    """Get an asynchronous database session."""
    async with AsyncSessionLocal() as db:
        yield db  # Yield the session to be used in route handlers
