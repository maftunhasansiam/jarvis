# packages/api/app/agent/logging.py
from typing import List, Optional
from ..db.base import SessionLocal
from ..db.models import TaskLog

def append_log(task_id: str, step_id: Optional[str], status: str, output: dict):
    db = SessionLocal()
    try:
        log = TaskLog(task_id=task_id, step_id=step_id, status=status, output=output)
        db.add(log)
        db.commit()
        db.refresh(log)
        return log
    finally:
        db.close()

def get_logs(task_id: str, limit: int = 200) -> List[dict]:
    db = SessionLocal()
    try:
        rows = db.query(TaskLog).filter(TaskLog.task_id == task_id).order_by(TaskLog.created_at.asc()).limit(limit).all()
        return [
            {
                "id": r.id,
                "task_id": r.task_id,
                "step_id": r.step_id,
                "status": r.status,
                "output": r.output,
                "created_at": r.created_at.isoformat() if r.created_at else None,
            }
            for r in rows
        ]
    finally:
        db.close()
