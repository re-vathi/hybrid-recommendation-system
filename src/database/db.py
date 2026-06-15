from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from src.database.models import Base

# Database URL - supports SQLite for dev, PostgreSQL for prod
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./recommendations.db")

# Create engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
    echo=False,
    pool_pre_ping=True
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Dependency for FastAPI routes"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)
    print("✓ Database initialized")

if __name__ == "__main__":
    init_db()