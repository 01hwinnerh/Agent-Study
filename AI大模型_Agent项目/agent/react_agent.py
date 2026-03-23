"""
ReactAgent智能体核心类：
核心作用：
1. 基于LangChain创建React模式的Agent（思考→行动→观察→重复）
2. 整合大模型、工具列表、中间件、动态提示词，实现智能工具调用+场景化回答
3. 支持流式输出（逐段返回模型回答），适配前端实时展示

适配目录结构：
- 当前文件位于 agent/ 文件夹
- model/、utils/、agent/tools/ 均为平级目录，导入无需加额外前缀
"""
# ====================== LangChain Agent核心导入 ======================
from langchain.agents import create_agent  # 创建React模式Agent的核心函数

# ====================== 自定义模块导入（适配平级目录） ======================
from model.factory import chat_model  # 导入预初始化的通义千问对话模型
from utils.prompt_loader import load_system_prompts  # 加载系统主提示词
# 导入所有Agent可调用的工具函数
from agent.tools.agent_tools import (
    rag_summarize, get_weather, get_user_location, get_user_id,
    get_current_month, fetch_external_data, fill_context_for_report
)
# 导入Agent中间件（工具监控、模型前日志、动态提示词切换）
from agent.tools.middleware import monitor_tool, log_before_model, report_prompt_switch


# ====================== ReactAgent核心类 ======================
class ReactAgent:
    """
    React模式Agent类：
    React = Reason（思考） + Act（行动）
    Agent会根据用户提问，自动思考需要调用的工具→执行工具→获取结果→生成回答
    核心特性：
    1. 整合所有自定义工具，支持智能选择调用
    2. 绑定中间件，实现工具监控、动态提示词切换
    3. 支持流式输出，逐段返回模型回答
    """

    def __init__(self):
        """
        初始化Agent：
        1. 创建Agent实例，绑定模型、提示词、工具、中间件
        2. 所有依赖一次性初始化，避免重复创建资源
        """
        self.agent = create_agent(
            model=chat_model,  # 绑定通义千问对话模型（预初始化的ChatTongyi实例）
            system_prompt=load_system_prompts(),  # 初始系统提示词（后续可被中间件动态替换）
            # 绑定Agent可调用的所有工具列表
            tools=[
                rag_summarize,  # RAG检索参考资料
                get_weather,  # 获取指定城市天气
                get_user_location,  # 获取用户所在城市
                get_user_id,  # 获取用户ID
                get_current_month,  # 获取当前月份
                fetch_external_data,  # 获取用户月度使用记录
                fill_context_for_report  # 触发报告场景上下文注入
            ],
            # 绑定中间件（按顺序执行：工具监控→模型前日志→动态提示词切换）
            middleware=[monitor_tool, log_before_model, report_prompt_switch],
        )

    def execute_stream(self, query: str):
        """
        核心方法：执行Agent并返回流式回答
        流程：
        1. 封装用户提问为Agent可识别的消息格式
        2. 调用Agent.stream实现流式输出
        3. 遍历流式返回结果，逐段yield给调用方

        参数：
            query: str - 用户的提问字符串（如"给我生成我的使用报告"）
        返回：
            Generator[str, None, None] - 流式生成的回答片段（逐段字符串）
        """
        # 步骤1：封装用户输入为Agent要求的格式
        # messages列表是Agent的核心输入，每个元素是包含role和content的字典
        # role="user"：标记为用户消息；content=query：用户的具体提问
        input_dict = {
            "messages": [
                {"role": "user", "content": query},
            ]
        }

        # 步骤2：调用Agent的stream方法实现流式输出
        # 参数说明：
        # - input_dict：Agent的输入（用户消息）
        # - stream_mode="values"：按值流式返回（而非按步骤）
        # - context={"report": False}：初始化运行时上下文，默认非报告场景
        #   （该context会被monitor_tool中间件修改，触发提示词切换）
        for chunk in self.agent.stream(input_dict, stream_mode="values", context={"report": False}):
            # 步骤3：提取最新一条消息（模型的流式回答片段）
            latest_message = chunk["messages"][-1]

            # 步骤4：过滤空内容，仅返回有效回答片段
            if latest_message.content:
                # yield：逐段返回结果（流式输出核心），添加换行符提升可读性
                yield latest_message.content.strip() + "\n"


# ====================== 测试代码 ======================
if __name__ == '__main__':
    # 1. 初始化ReactAgent实例（自动创建Agent、绑定工具/中间件）
    agent = ReactAgent()

    # 2. 调用execute_stream，传入测试提问（生成使用报告）
    # 3. 遍历流式返回的回答片段，实时打印（flush=True强制刷新输出）
    for chunk in agent.execute_stream("在我当前的城市天气情况下，我应该怎么保养我的扫地机器人"):
        print(chunk, end="", flush=True)