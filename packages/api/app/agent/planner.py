from typing import List
from packages.api.app.models.agent_models import PlanStep
import uuid

class Planner:
    """Simple stub planner:
       - maps goal keywords to safe tool actions (echo, http_request)
       - returns a list of PlanStep
    """
    def __init__(self):
        # mapping keywords -> tool name
        self.mapping = {
            "fetch": "http_request",
            "get": "http_request",
            "echo": "echo",
            "say": "echo",
        }

    def plan(self, goal: str, context: dict) -> List[PlanStep]:
        goal_l = goal.lower()
        steps = []
        # simple heuristic: if any mapping keyword is in goal -> use that tool
        for kw, tool in self.mapping.items():
            if kw in goal_l:
                step = PlanStep(
                    id=str(uuid.uuid4()),
                    action=tool,
                    input={"goal": goal, "context": context},
                    requires_approval=False,
                )
                steps.append(step)
        # fallback: return a single echo step if nothing matched
        if not steps:
            steps.append(PlanStep(
                id=str(uuid.uuid4()),
                action="echo",
                input={"message": f"Planned (fallback) for goal: {goal}"},
                requires_approval=False,
            ))
        return steps
