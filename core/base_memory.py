# core/base_memory.py
from abc import ABC, abstractmethod
from typing import Any

class BaseMemory(ABC):
    @abstractmethod
    def save(self, key: str, value: Any):
        pass

    @abstractmethod
    def load(self, key: str) -> Any:
        pass

    @abstractmethod
    def clear(self):
        pass