# agents/react_agent.py
from core.base_agent import BaseAgent
from typing import Dict, Any

class ReActAgent(BaseAgent):
    def __init__(self, name: str, memory=None, tools: list = None):
        super().__init__(name, "react", memory, tools)
        self.function_call = True
        self.mcp_enabled = True

    def invoke(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        question = input_data.get("question", "")
        thought = f"I need to answer: {question}"
        action = "Use DeepSeek to generate answer"
        tool = next((t for t in self.tools if t.name == "deepseek_inference"), None)
        if not tool:
            return {"error": "Tool not available"}

        observation = tool.run(prompt=question)
        final_answer = f"Thought: {thought}\nAction: {action}\nObservation: {observation}\nAnswer: {observation}"

        return {"response": final_answer}