# core/base_agent.py
from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseAgent(ABC):
    def __init__(self, name: str, agent_type: str, memory=None, tools: list = None):
        self.name = name
        self.agent_type = agent_type
        self.memory = memory
        self.tools = tools or []
        self.config = {}

    @abstractmethod
    def invoke(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        pass

    def add_tool(self, tool):
        self.tools.append(tool)

    def has_function_call(self) -> bool:
        return hasattr(self, "function_call") and self.function_call

    def has_mcp(self) -> bool:
        return hasattr(self, "mcp_enabled") and self.mcp_enabled