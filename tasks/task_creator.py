# tasks/task_creator.py
from core.base_task import BaseTask
from enums.task_types import TaskType
from config.settings import settings
import json
import os

class TaskCreator:
    @staticmethod
    def create_task(task_type: TaskType, config: dict = None) -> BaseTask:
        # 实际项目中应使用工厂模式
        task = BaseTask(task_type=task_type, config=config)
        return task

    @staticmethod
    def create_dialogue_task(config: dict) -> BaseTask:
        task = BaseTask(task_type=TaskType.DIALOGUE, config=config)
        filepath = os.path.join(settings.TASK_STORAGE_DIR, f"{task.task_id}.json")
        task.save_to_json(filepath)
        return task