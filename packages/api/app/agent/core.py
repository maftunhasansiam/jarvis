from packages.api.app.agent.executor import Executor
from packages.api.app.models.agent_models import ExecutionResult
from typing import Dict, List

class ExecutorCore:
    """High-level wrapper maintaining in-memory tasks and statuses."""
    def __init__(self):
        self.executor = Executor()
        self.tasks: Dict[str, Dict] = {}        # task_id -> {status, results, logs}

    def execute_step(self, step, task_id: str = None) -> ExecutionResult:
        res = self.executor.run(step)
        if task_id:
            if task_id not in self.tasks:
                self.tasks[task_id] = {"status": "running", "results": [], "logs": []}
            self.tasks[task_id]["results"].append(res.model_dump())
            self.tasks[task_id]["logs"].append(
                {"step_id": step.id, "status": res.status}
            )
            self.tasks[task_id]["status"] = "success" if res.status == "success" else "error"
        return res

    def get_task_status(self, task_id: str):
        return self.tasks.get(task_id)
