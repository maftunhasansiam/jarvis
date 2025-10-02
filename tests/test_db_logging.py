# packages/api/tests/test_db_logging.py
import os
import tempfile
import pytest
from packages.api.app.db.base import init_db, engine, SessionLocal
from packages.api.app.db.models import Task, TaskLog
from packages.api.app.agent.logging import append_log, get_logs

def test_db_and_logging(tmp_path):
    # use sqlite file in tmp to avoid collisions
    db_file = tmp_path / "test_db.db"
    os.environ["JARVIS_DATABASE_URL"] = f"sqlite:///{db_file}"
    # re-import init functions if needed in your project
    init_db()

    # persist a task row manually
    db = SessionLocal()
    try:
        t = Task(id="task-test-1", goal="testing", status="planned")
        db.add(t)
        db.commit()
    finally:
        db.close()

    log = append_log("task-test-1", "step-1", "ok", {"out": "done"})
    assert log.task_id == "task-test-1"
    logs = get_logs("task-test-1")
    assert len(logs) >= 1
    assert logs[-1]["status"] == "ok"
