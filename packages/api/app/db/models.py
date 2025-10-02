# packages/api/app/db/models.py
from sqlalchemy import Column, String, Integer, DateTime, Text, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.sql import func
import uuid

from ..db.base import Base


def gen_uuid():
    return str(uuid.uuid4())


class Task(Base):
    __tablename__ = "tasks"
    id = Column(String, primary_key=True, default=gen_uuid)
    goal = Column(Text, nullable=False)
    status = Column(String, default="created", index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class TaskLog(Base):
    __tablename__ = "task_logs"
    id = Column(String, primary_key=True, default=gen_uuid)
    task_id = Column(String, ForeignKey("tasks.id"), index=True, nullable=False)
    step_id = Column(String, nullable=True)
    status = Column(String, nullable=False)
    output = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
