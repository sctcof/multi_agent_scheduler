# memory/text_memory.py
import json
from core.base_memory import BaseMemory
from config.settings import settings
from typing import Dict, Any

class TextMemory(BaseMemory):
    def __init__(self, filepath: str = None):
        self.filepath = filepath or settings.MEMORY_STORAGE_FILE
        self.data = self._load_from_file()

    def _load_from_file(self):
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _save_to_file(self):
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def save(self, key: str, value: Any):
        self.data[key] = value
        self._save_to_file()

    def load(self, key: str) -> Any:
        return self.data.get(key)

    def clear(self):
        self.data.clear()
        self._save_to_file()