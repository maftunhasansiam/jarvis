from fastapi import APIRouter, HTTPException
from uuid import uuid4

from ..db.base import init_db, SessionLocal
from ..db.models import Task
from ..agent.llm_adapter import LLMAdapter
from ..agent.logging import append_log, get_logs
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
init_db()
planner = Planner()
executor = ExecutorCore()


@router.post("/v1/agent/plan")
def plan_endpoint(req: PlanRequest):
    adapter = LLMAdapter()
    plan = adapter.generate_plan(req.goal, req.context)

    # persist task
    db = SessionLocal()
    try:
        t = Task(id=plan["task_id"], goal=req.goal, status="planned")
        db.add(t)
        db.commit()
    finally:
        db.close()

    append_log(plan["task_id"], None, "planned", {"plan": plan})
    return plan


@router.post("/plan", response_model=PlanResponse)
def plan_goal(req: PlanRequest):
    plan = planner.plan(req.goal, req.context or {})
    task_id = str(uuid4())
    return PlanResponse(task_id=task_id, steps=plan)


@router.post("/execute")
def execute(req: ExecuteRequest):
    task_id = req.task_id or str(uuid4())
    results = []
    for step in req.steps:
        res = executor.execute_step(step, task_id)
        append_log(task_id, step.id, res.status, res.output)
        results.append(res)
    return {"task_id": task_id, "results": results}


@router.get("/status/{task_id}")
def get_task_status(task_id: str):
    status = executor.get_task_status(task_id)
    if status is None:
        raise HTTPException(status_code=404, detail="task not found")
    return {"task_id": task_id, "status": status}


@router.get("/status")
def get_logs_status(task_id: str):
    logs = get_logs(task_id)
    return {"task_id": task_id, "logs": logs}
