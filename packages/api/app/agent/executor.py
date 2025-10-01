from packages.api.app.models.agent_models import PlanStep, ExecutionResult
from packages.api.app.agent.tools import registry
from typing import Any, Dict

class Executor:
    """Executes a single PlanStep using the tools registry.
       Only registered tools can be executed.
    """
    def __init__(self):
        self.registry = registry

    def run(self, step: PlanStep) -> ExecutionResult:
        tool = self.registry.get(step.action)
        if not tool:
            return ExecutionResult(step_id=step.id, status="error", output={"error": "tool_not_found"})
        try:
            output = tool.run(step.input)
            return ExecutionResult(step_id=step.id, status="success", output=output)
        except Exception as e:
            return ExecutionResult(step_id=step.id, status="error", output={"error": str(e)})
