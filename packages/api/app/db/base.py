# packages/api/app/db/base.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE_URL = os.getenv("JARVIS_DATABASE_URL", "sqlite:///./jarvis_dev.db")

# echo=True useful for debugging
engine = create_engine(
    DATABASE_URL,
    connect_args=(
        {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
    ),
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def init_db():
    from .models import Task, TaskLog

    Base.metadata.create_all(bind=engine)
