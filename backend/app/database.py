from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import DATABASE_URL
import logging

logger = logging.getLogger(__name__)

engine = create_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=40,
    echo=False,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)
    logger.info("Database initialized")
