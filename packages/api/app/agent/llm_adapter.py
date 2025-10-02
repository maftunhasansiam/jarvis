# packages/api/app/agent/llm_adapter.py
"""
Safe LLM Adapter stub. Does NOT call external LLMs.
Provides an interface for planner to request plans from a 'model'.
"""

from typing import List, Dict
import uuid

def make_step(action: str, input: Dict, requires_approval: bool = False):
    return {
        "id": str(uuid.uuid4()),
        "action": action,
        "input": input,
        "requires_approval": requires_approval,
    }

class LLMAdapter:
    def __init__(self, provider_cfg: dict = None):
        # provider_cfg reserved for future wiring (kept empty by default)
        self.cfg = provider_cfg or {}

    def generate_plan(self, goal: str, context: dict = None) -> Dict:
        """
        Return a predictable stub PlanResponse so tests and planner can rely on it.
        Example: If `fetch` in goal -> http_request step; else echo step.
        """
        context = context or {}
        goal_lower = goal.lower()
        steps = []

        if "fetch" in goal_lower or "get" in goal_lower or "download" in goal_lower:
            steps.append(make_step("http_request", {"url": "https://example.com"}, requires_approval=False))
        else:
            steps.append(make_step("echo", {"message": f"Plan for goal: {goal}"}))

        return {
            "task_id": str(uuid.uuid4()),
            "steps": steps
        }

# Usage:
# adapter = LLMAdapter()
# plan = adapter.generate_plan("Fetch website")
