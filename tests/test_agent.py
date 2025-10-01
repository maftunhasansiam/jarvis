from fastapi.testclient import TestClient
from packages.api.app.main import app
import json

client = TestClient(app)


def test_health():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json()["msg"].startswith("Jarvis Agent API")


def test_plan_echo_fallback():
    payload = {"goal": "do something unknown"}
    r = client.post("/v1/agent/plan", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert "task_id" in data
    assert isinstance(data["steps"], list)
    assert data["steps"][0]["action"] == "echo"


def test_plan_http_mapping():
    payload = {"goal": "fetch https://httpbin.org/get"}
    r = client.post("/v1/agent/plan", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert any(s["action"] == "http_request" for s in data["steps"])


def test_execute_echo():
    payload = {
        "task_id": "t1",
        "steps": [{"id": "1", "action": "echo", "input": {"message": "Hello"}}],
    }
    r = client.post("/v1/agent/execute", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["results"][0]["output"]["echo"] == "Hello"


def test_execute_http_request():
    payload = {
        "task_id": "t2",
        "steps": [
            {
                "id": "2",
                "action": "http_request",
                "input": {"url": "https://httpbin.org/get"},
            }
        ],
    }
    r = client.post("/v1/agent/execute", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["results"][0]["status"] == "success"
    assert "status_code" in data["results"][0]["output"]
