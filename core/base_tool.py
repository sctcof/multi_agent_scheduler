# core/base_tool.py
from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseTool(ABC):
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    @abstractmethod
    def run(self, **kwargs) -> Any:
        pass