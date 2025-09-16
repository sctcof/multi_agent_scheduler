# workflows/workflow_executor.py
from .workflow import Workflow, Node, Edge
from agents.agent_factory import AgentFactory
from memory.text_memory import TextMemory
from tools.deepseek_tool import DeepSeekTool
from commons.constants import AgentType
import asyncio

class WorkflowExecutor:
    def __init__(self, workflow: Workflow):
        self.workflow = workflow
        self.agents = {}
        self._build_agents()

    def _build_agents(self):
        tool = DeepSeekTool()
        memory = TextMemory()
        for node in self.workflow.nodes:
            # print("node.agent_type.upper():",node.agent_type.upper())
            agent_type = AgentType(node.agent_type.upper())
            agent = AgentFactory.create_agent(
                agent_type=agent_type,
                name=f"agent_{node.id}",
                memory=memory,
                tools=[tool]
            )
            self.agents[node.id] = agent

    async def execute_async(self, input_data: dict):
        current_node_id = self.workflow.start_node
        data = input_data

        while current_node_id:
            node = next(n for n in self.workflow.nodes if n.id == current_node_id)
            agent = self.agents[node.id]
            result = agent.invoke({"context": data.get("context", ""), "question": data.get("question", "")})
            data.update(result)

            # 找下一个节点
            next_edge = next((e for e in self.workflow.edges if e.source == current_node_id), None)
            current_node_id = next_edge.target if next_edge else None

        return data

    def execute_sync(self, input_data: dict):
        return asyncio.run(self.execute_async(input_data))