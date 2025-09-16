# enums/task_types.py
from enum import Enum

class TaskType(Enum):
    SINGLE = "single"
    PLAN = "plan"
    DIALOGUE = "dialogue"