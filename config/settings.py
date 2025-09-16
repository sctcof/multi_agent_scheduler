# config/settings.py
import os
from dataclasses import dataclass

@dataclass
class Settings:
    DEEPSEEK_API_KEY: str = os.getenv("DEEPSEEK_API_KEY", "")
    DEEPSEEK_API_BASE: str = "https://api.deepseek.com/v1"
    VECTOR_DB_PATH: str = "multi_agent_scheduler/data/vector_store"
    TASK_STORAGE_DIR: str = "multi_agent_scheduler/data/tasks_storage"
    MEMORY_STORAGE_FILE: str = "multi_agent_scheduler/data/memory/dialogue_history.json"
    WORKFLOW_YAML_DIR: str = "multi_agent_scheduler/data/workflows/yaml"

settings = Settings()

# 确保目录存在
import os
for path in [settings.TASK_STORAGE_DIR, settings.VECTOR_DB_PATH, os.path.dirname(settings.MEMORY_STORAGE_FILE), settings.WORKFLOW_YAML_DIR]:
    os.makedirs(path, exist_ok=True)