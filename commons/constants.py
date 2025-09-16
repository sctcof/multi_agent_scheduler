# common/constants.py
from enum import Enum

class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class AgentType(Enum):
    LONG_COT = "LONG_COT"
    REACT = "REACT"

class MemoryType(Enum):
    TEXT = "text"
    VECTOR = "vector"
    DATABASE = "database"