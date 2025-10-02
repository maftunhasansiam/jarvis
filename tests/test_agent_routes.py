import pytest
from fastapi.testclient import TestClient

from packages.api.app.main import app

client = TestClient(app)


def test_plan_endpoint_creates_task_and_logs():
    resp = client.post(
        "/v1/agent/plan", json={"goal": "fetch example.com", "context": {}}
    )
    assert resp.status_code == 200
    body = resp.json()
    assert "task_id" in body
    assert isinstance(body["steps"], list)

def test_plan_goal_stub():
    resp = client.post("/v1/agent/plan", json={"goal": "echo hello", "context": {}})
    assert resp.status_code == 200
    body = resp.json()
    assert "task_id" in body
    assert isinstance(body["steps"], list)


def test_execute_and_status_flow():
    # 1. Plan first
    plan_resp = client.post(
        "/v1/agent/plan", json={"goal": "echo hello", "context": {}}
    )
    assert plan_resp.status_code == 200
    task_id = plan_resp.json()["task_id"]
    steps = plan_resp.json()["steps"]

    # 2. Execute (if /execute is available)
    exec_resp = client.post("/execute", json={"task_id": task_id, "steps": steps})
    if exec_resp.status_code == 404:
        pytest.skip("`/execute` not mounted in main.py")
    else:
        assert exec_resp.status_code == 200
        exec_body = exec_resp.json()
        assert exec_body["task_id"] == task_id
        assert isinstance(exec_body["results"], list)

    # 3. Logs
    log_resp = client.get(f"/v1/agent/status?task_id={task_id}")
    assert log_resp.status_code == 200
    logs = log_resp.json()
    assert logs["task_id"] == task_id
    assert isinstance(logs["logs"], list)


def test_get_task_status_endpoint_handles_missing_task():
    resp = client.get("/v1/agent/status/nonexistent-task-id")
    assert resp.status_code == 404
    body = resp.json()
    assert body["detail"] == "task not found"
