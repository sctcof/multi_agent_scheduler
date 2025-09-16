# agents/agent_factory.py
from .long_cot_agent import LongCoTAgent
from .react_agent import ReActAgent
from commons.constants import AgentType

class AgentFactory:
    @staticmethod
    def create_agent(agent_type: AgentType, name: str, memory=None, tools: list = None):
        if agent_type == AgentType.LONG_COT:
            return LongCoTAgent(name, memory, tools)
        elif agent_type == AgentType.REACT:
            return ReActAgent(name, memory, tools)
        else:
            raise ValueError(f"Unknown agent type: {agent_type}")