# tools/deepseek_tool.py
from core.base_tool import BaseTool
from langchain_deepseek import ChatDeepSeek
from langchain_core.messages import HumanMessage
from config.settings import settings
import os

class DeepSeekTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="deepseek_inference",
            description="Call DeepSeek LLM for text generation using langchain-deepseek"
        )
        # 设置 API Key
        api_key = settings.DEEPSEEK_API_KEY
        if not api_key or api_key == "your-deepseek-key":
            raise ValueError("请在环境变量或 settings.py 中设置有效的 DEEPSEEK_API_KEY")

        # 初始化 ChatDeepSeek 模型
        self.model = ChatDeepSeek(
            model="deepseek-chat",  # 可选: deepseek-chat, deepseek-coder
            temperature=0.7,
            max_tokens=512,
            api_key=api_key,
            base_url=settings.DEEPSEEK_API_BASE  # 可选自定义 base_url
        )

    def run(self, prompt: str, **kwargs) -> str:
        """
        使用 ChatDeepSeek 发送消息并获取回复
        :param prompt: 输入提示
        :return: 模型生成的回复文本
        """
        try:
            # 构造消息
            message = HumanMessage(content=prompt)
            # 调用模型
            response = self.model.invoke([message])
            # 返回内容
            return response.content.strip()
        except Exception as e:
            return f"Error calling DeepSeek via LangChain: {str(e)}"

    # 在 DeepSeekTool 中添加 stream 方法
    def stream(self, prompt: str):
        message = HumanMessage(content=prompt)
        return self.model.stream([message])