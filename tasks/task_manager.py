# tasks/task_manager.py
from core.base_task import BaseTask
from config.settings import settings
import os
import json
from typing import Dict, Any
from enums.task_types import TaskType

class TaskManager:
    def __init__(self):
        self.tasks: Dict[str, BaseTask] = {}

    def load_all_tasks(self):
        for filename in os.listdir(settings.TASK_STORAGE_DIR):
            if filename.endswith(".json"):
                filepath = os.path.join(settings.TASK_STORAGE_DIR, filename)
                # 简化加载（实际需重构具体任务类型）
                with open(filepath, 'r') as f:
                    data = json.load(f)
                # 可扩展为任务工厂
                print(f"Loaded task: {data['task_id']}")

    def get_task(self, task_id: str) -> BaseTask:
        # 实际从存储加载
        filepath = os.path.join(settings.TASK_STORAGE_DIR, f"{task_id}.json")
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                data = json.load(f)
            # 重构任务对象
            task_type = TaskType(data["task_type"])
            task = BaseTask(task_type, data["config"])
            task.task_id = data["task_id"]
            task.status = next(st for st in ["pending", "running", "completed", "failed"] if st == data["status"])
            task.result = data["result"]
            return task
        return None