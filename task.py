"""
Task Manager — tracks long-running async backend jobs.
Used for graph extraction, simulation prep, and report generation.
"""

import uuid
import time
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Task:
    task_id: str
    task_type: str                    # e.g. "graph_build", "report_generate"
    status: str = "pending"           # pending | running | complete | failed
    progress_pct: int = 0             # 0–100
    message: str = ""
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)
    result: Optional[dict] = None
    error: Optional[str] = None

    def to_dict(self):
        return {
            "task_id": self.task_id,
            "task_type": self.task_type,
            "status": self.status,
            "progress_pct": self.progress_pct,
            "message": self.message,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "result": self.result,
            "error": self.error,
        }


class TaskManager:
    """
    In-memory task registry.
    For production, replace with Redis or a database backend.
    """

    def __init__(self):
        self._tasks: dict[str, Task] = {}

    def create_task(self, task_type: str) -> str:
        task_id = str(uuid.uuid4())
        self._tasks[task_id] = Task(task_id=task_id, task_type=task_type)
        return task_id

    def get_task(self, task_id: str) -> Optional[Task]:
        return self._tasks.get(task_id)

    def update_task(
        self,
        task_id: str,
        status: str = None,
        progress_pct: int = None,
        message: str = None,
        result: dict = None,
        error: str = None,
    ):
        task = self._tasks.get(task_id)
        if not task:
            return
        if status is not None:
            task.status = status
        if progress_pct is not None:
            task.progress_pct = progress_pct
        if message is not None:
            task.message = message
        if result is not None:
            task.result = result
        if error is not None:
            task.error = error
            task.status = "failed"
        task.updated_at = time.time()

    def complete_task(self, task_id: str, result: dict = None):
        self.update_task(task_id, status="complete", progress_pct=100, result=result)

    def fail_task(self, task_id: str, error: str):
        self.update_task(task_id, error=error)
