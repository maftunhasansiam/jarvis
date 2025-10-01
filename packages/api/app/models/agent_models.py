from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional
from uuid import UUID

class PlanRequest(BaseModel):
    goal: str
    context: Optional[Dict[str, Any]] = Field(default_factory=dict)

class PlanStep(BaseModel):
    id: str
    action: str
    input: Dict[str, Any]
    requires_approval: bool = False

class PlanResponse(BaseModel):
    task_id: str
    steps: List[PlanStep]

class ExecuteRequest(BaseModel):
    task_id: Optional[str] = None
    steps: List[PlanStep]

class ExecutionResult(BaseModel):
    step_id: str
    status: str
    output: Dict[str, Any]

class TaskStatus(BaseModel):
    task_id: str
    status: str
