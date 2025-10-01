from fastapi import APIRouter, HTTPException
from uuid import uuid4
from packages.api.app.agent.planner import Planner
from packages.api.app.agent.core import ExecutorCore
from packages.api.app.models.agent_models import (
    PlanRequest,
    ExecuteRequest,
    PlanResponse,
    ExecutionResult,
    TaskStatus,
)

router = APIRouter()

planner = Planner()
executor = ExecutorCore()


@router.post("/plan", response_model=PlanResponse)
def plan_goal(req: PlanRequest):
    plan = planner.plan(req.goal, req.context or {})
    task_id = str(uuid4())
    return PlanResponse(task_id=task_id, steps=plan)


@router.post("/execute")
def execute(req: ExecuteRequest):
    results = []
    for step in req.steps:
        res = executor.execute_step(step, req.task_id or "adhoc")
        results.append(res)
    return {"results": results}


@router.get("/status/{task_id}")
def status(task_id: str):
    # In-memory status is exposed from executor
    status = executor.get_task_status(task_id)
    if status is None:
        raise HTTPException(status_code=404, detail="task not found")
    return {"task_id": task_id, "status": status}
