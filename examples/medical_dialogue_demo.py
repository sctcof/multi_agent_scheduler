# examples/medical_dialogue_demo.py
from memory.text_memory import TextMemory
from agents.agent_factory import AgentFactory
from commons.constants import AgentType
from tools.deepseek_tool import DeepSeekTool
from workflows.workflow import Workflow, Node, Edge
from workflows.workflow_parser import WorkflowParser
from workflows.workflow_executor import WorkflowExecutor
from tasks.task_creator import TaskCreator
from enums.task_types import TaskType
from config.settings import settings
import asyncio

# 必需字段
REQUIRED_FIELDS = ["name", "age", "symptoms", "duration"]

def check_completeness(data: dict) -> tuple:
    missing = [field for field in REQUIRED_FIELDS if not data.get(field)]
    return len(missing) == 0, missing

# ✅ 将整个对话流程改为 async 函数
async def medical_dialogue_flow():
    print("启动医疗多轮对话系统...")
    memory = TextMemory()
    tool = DeepSeekTool()

    # 创建并保存流程（仅一次）
    workflow_file = f"{settings.WORKFLOW_YAML_DIR}/medical.yaml"
    if not hasattr(medical_dialogue_flow, "workflow_created"):
        workflow = Workflow("medical_intake")
        workflow.add_node(Node(id="nurse", agent_type="react", config={"role": "intake nurse"}))
        workflow.add_node(Node(id="doctor", agent_type="long_cot", config={"role": "diagnostician"}))
        workflow.add_edge(Edge(source="nurse", target="doctor"))
        workflow.save_to_yaml(workflow_file)
        medical_dialogue_flow.workflow_created = True

    # 加载流程并创建执行器
    loaded_workflow = WorkflowParser.from_file(workflow_file)
    executor = WorkflowExecutor(loaded_workflow)

    patient_data = {}
    print("👩‍⚕️ 您好，我是您的健康助手，请描述您的症状。（输入 'quit' 退出）")

    #如果需要支持流式输出，可以采用这个方案
    # # 示例：流式输出（在 async 函数中）
    # async for chunk in tool.stream("请写一首关于春天的诗"):
    #     print(chunk.content, end="", flush=True)

    history = memory.load("conversation") or []
    while True:
        user_input = input(" user_input: ").strip()
        if user_input.lower() == 'quit':
            break

        # 添加用户输入到历史
        history.append(f"患者: {user_input}")
        memory.save("conversation", history)

        try:
            # ✅ 正确方式：使用 await 调用异步方法
            result = await executor.execute_async({
                "context": "\n".join(history[-6:]),
                "question": user_input
            })
        except Exception as e:
            print(f"执行出错: {e}")
            continue

        response = result.get("response", "抱歉，我没有理解。")
        print(f"医生: {response}")

        # 简单模拟信息提取（实际可用 NLP）
        for field in REQUIRED_FIELDS:
            if field in user_input and not patient_data.get(field):
                patient_data[field] = user_input

        # 检查完整性
        complete, missing = check_completeness(patient_data)
        if not complete:
            follow_up = f"为了更好地帮助您，请补充以下信息: {', '.join(missing)}"
            print(f"医生: {follow_up}")
            history.append(f"医生: {follow_up}")
            memory.save("conversation", history)
        else:
            print("✅ 信息完整，正在生成综合诊断建议...")
            final_prompt = "基于以上病史，请给出初步诊断、可能病因和就医建议。"
            final_result = await executor.execute_async({
                "context": "\n".join(history),
                "question": final_prompt
            })
            print("\n📋 诊断建议:\n", final_result.get("response", "无建议"))
            break

# ✅ 主函数必须也用 asyncio.run() 启动
if __name__ == "__main__":
    asyncio.run(medical_dialogue_flow())  # ✅ 正确启动异步主函数