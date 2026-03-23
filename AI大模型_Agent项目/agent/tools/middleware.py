"""
Agent中间件（Middleware）集合：
核心作用：
1. 监控工具调用（记录工具名称/参数/执行结果）
2. 模型调用前日志记录（跟踪Agent状态和消息）
3. 动态切换提示词（根据上下文判断是否为报告生成场景，切换对应提示词）

LangChain Middleware说明：
- wrap_tool_call：装饰工具调用函数，拦截工具执行的前后逻辑
- before_model：模型调用前执行的钩子函数
- dynamic_prompt：模型调用前动态修改提示词的钩子函数
"""
# ====================== 类型/基础库导入 ======================
from typing import Callable  # 类型注解：标记可调用函数类型

# ====================== 自定义模块导入（适配平级目录结构） ======================
# 提示词加载工具：加载系统主提示词/报告生成提示词
from utils.prompt_loader import load_system_prompts, load_report_prompts
# 自定义日志器：记录中间件执行日志（INFO/DEBUG/ERROR级别）
from utils.logger_handler import logger

# ====================== LangChain/LangGraph核心类型导入 ======================
from langchain.agents import AgentState  # Agent的核心状态：存储消息/工具调用记录等
from langchain.agents.middleware import (
    wrap_tool_call,  # 工具调用装饰器：拦截工具执行流程
    before_model,  # 模型调用前钩子：模型执行前触发
    dynamic_prompt,  # 动态提示词钩子：生成提示词前触发
    ModelRequest  # 模型请求封装：包含运行时上下文/提示词等
)
from langchain.tools.tool_node import ToolCallRequest  # 工具调用请求：封装工具名称/参数等
from langchain_core.messages import ToolMessage  # 工具调用返回结果：标准化工具输出格式
from langgraph.runtime import Runtime  # LangGraph运行时：记录执行上下文
from langgraph.types import Command  # LangGraph命令：工具调用的返回类型之一


# ====================== 中间件1：工具调用监控 ======================
@wrap_tool_call  # 装饰器：拦截所有工具调用，执行该函数的逻辑
def monitor_tool(
        # 参数1：工具调用请求封装（包含工具名称、参数、运行时上下文等）
        request: ToolCallRequest,
        # 参数2：原始的工具执行函数（被装饰的工具函数本身）
        handler: Callable[[ToolCallRequest], ToolMessage | Command],
) -> ToolMessage | Command:  # 返回值：工具执行结果（ToolMessage）或LangGraph命令
    """
    工具调用监控中间件：
    核心功能：
    1. 记录工具调用的名称、参数、执行结果（成功/失败）
    2. 识别"fill_context_for_report"工具调用，标记报告生成上下文
    3. 捕获工具执行异常，记录错误日志并抛出

    参数：
        request: ToolCallRequest - 工具调用请求对象，包含：
            - request.tool_call["name"]：工具名称（如"fetch_external_data"）
            - request.tool_call["args"]：工具入参（如{"user_id":"1001","month":"2025-01"}）
            - request.runtime.context：运行时上下文字典（可存储自定义状态）
        handler: 原始工具执行函数，调用后返回工具执行结果
    返回：
        ToolMessage | Command：工具执行结果（原样返回handler的输出）
    异常：
        Exception：工具执行失败时，记录错误日志并重新抛出异常
    """
    # 步骤1：记录工具调用的基本信息（便于调试/审计）
    logger.info(f"[tool monitor]执行工具：{request.tool_call['name']}")
    logger.info(f"[tool monitor]传入参数：{request.tool_call['args']}")

    try:
        # 步骤2：执行原始工具函数，获取结果
        result = handler(request)
        logger.info(f"[tool monitor]工具{request.tool_call['name']}调用成功")

        # 步骤3：识别报告生成上下文触发工具，标记运行时上下文
        # 当调用fill_context_for_report工具时，在runtime.context中标记report=True
        # 供dynamic_prompt钩子函数识别，切换为报告生成提示词
        if request.tool_call['name'] == "fill_context_for_report":
            request.runtime.context["report"] = True            ###     request.runtime.context：框架自带的「空字典容器」，自己定义往里面放什么实现动态提示词切换

        # 步骤4：原样返回工具执行结果，不干扰核心流程
        return result
    except Exception as e:
        # 步骤5：捕获工具执行异常，记录详细错误日志
        logger.error(f"工具{request.tool_call['name']}调用失败，原因：{str(e)}")
        raise e  # 重新抛出异常，让Agent感知工具调用失败


# ====================== 中间件2：模型调用前日志记录 ======================
@before_model  # 装饰器：模型生成回答前触发该函数
def log_before_model(
        state: AgentState,  # Agent的完整状态：包含所有消息/工具调用记录/上下文
        runtime: Runtime,  # LangGraph运行时：记录执行流程的上下文信息
):
    """
    模型调用前日志中间件：
    核心功能：在大模型生成回答前，记录当前Agent状态和最新消息，便于调试

    参数：
        state: AgentState - Agent的核心状态对象，关键属性：
            - state['messages']：Agent的消息列表（用户提问/工具返回/模型回复等）
        runtime: Runtime - LangGraph运行时对象，包含执行上下文
    返回：
        None：仅记录日志，不修改状态/请求
    """
    # 记录当前消息列表的长度（便于判断消息数量是否异常）
    logger.info(f"[log_before_model]即将调用模型，带有{len(state['messages'])}条消息。")

    # 记录最新一条消息的类型和内容（DEBUG级别，仅调试时输出）
    # type(state['messages'][-1]).__name__：获取消息类型（如HumanMessage/ToolMessage）
    # state['messages'][-1].content.strip()：去除首尾空白的消息内容
    logger.debug(f"[log_before_model]{type(state['messages'][-1]).__name__} | {state['messages'][-1].content.strip()}")

    return None


# ====================== 中间件3：动态切换提示词 ======================
@dynamic_prompt  # 装饰器：模型生成提示词前触发，可动态替换提示词内容
def report_prompt_switch(request: ModelRequest):
    """
    动态提示词切换中间件：
    核心功能：根据运行时上下文判断是否为报告生成场景，切换对应的提示词
    - 报告场景：使用load_report_prompts()加载报告生成提示词
    - 普通场景：使用load_system_prompts()加载系统主提示词

    参数：
        request: ModelRequest - 模型请求对象，关键属性：
            - request.runtime.context：运行时上下文字典（由monitor_tool中间件设置）
    返回：
        str：切换后的提示词文本（供模型使用）
    """
    # 步骤1：从运行时上下文获取report标记（默认False）
    # 该标记由monitor_tool中间件在调用fill_context_for_report工具时设置为True
    is_report = request.runtime.context.get("report", False)

    # 步骤2：根据标记切换提示词
    if is_report:
        # 报告生成场景：返回报告专用提示词
        return load_report_prompts()
    # 普通场景：返回系统主提示词
    return load_system_prompts()