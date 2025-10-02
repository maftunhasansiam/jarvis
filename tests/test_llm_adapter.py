# packages/api/tests/test_llm_adapter.py
import pytest
from packages.api.app.agent.llm_adapter import LLMAdapter

def test_llm_adapter_returns_plan():
    adapter = LLMAdapter()
    plan = adapter.generate_plan("Do an echo test")
    assert "task_id" in plan
    assert isinstance(plan["steps"], list)
    assert plan["steps"][0]["action"] in ("echo", "http_request")
