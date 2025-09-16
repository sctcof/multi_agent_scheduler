# agents/long_cot_agent.py
from core.base_agent import BaseAgent
from typing import Dict, Any

class LongCoTAgent(BaseAgent):
    def __init__(self, name: str, memory=None, tools: list = None):
        super().__init__(name, "long_cot", memory, tools)
        self.function_call = True
        self.mcp_enabled = True

    def invoke(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        context = input_data.get("context", "")
        if self.memory:
            history = self.memory.load("conversation")
            if history:
                context = "\n".join(history[-5:]) + "\n" + context

        prompt = f"Reason step-by-step:\n{context}\nProvide a detailed answer."
        tool = next((t for t in self.tools if t.name == "deepseek_inference"), None)
        if not tool:
            return {"error": "DeepSeek tool not found"}

        result = tool.run(prompt=prompt)
        return {"response": result}