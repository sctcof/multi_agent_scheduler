# core/base_task.py
import json
import uuid
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Any, List
from commons.constants import TaskStatus
from enums.task_types import TaskType

class BaseTask(ABC):
    def __init__(self, task_type: TaskType, config: Dict[str, Any] = None):
        self.task_id = str(uuid.uuid4())
        self.task_type = task_type
        self.status = TaskStatus.PENDING
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.config = config or {}
        self.result = None
        self.error = None

    @abstractmethod
    def execute(self) -> Any:
        pass

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "task_type": self.task_type.value,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "config": self.config,
            "result": self.result,
            "error": self.error
        }

    def save_to_json(self, filepath: str):
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)

    @classmethod
    def load_from_json(cls, filepath: str) -> 'BaseTask':
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        # 重构对象（需子类实现）
        raise NotImplementedError("Subclass must implement load_from_json")

    def update_status(self, status: TaskStatus):
        self.status = status
        self.updated_at = datetime.now()