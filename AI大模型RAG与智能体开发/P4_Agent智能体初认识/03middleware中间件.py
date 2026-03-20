from langchain.agents import create_agent, AgentState
from langchain.agents.middleware import before_agent, after_agent, before_model, after_model, wrap_model_call, wrap_tool_call
from langchain_community.chat_models import ChatTongyi
from langchain_core.tools import tool
from langgraph.runtime import Runtime


@tool(description="查询天气，传入城市名称字符串，返回字符串天气信息")
def get_weather(city:str) -> str:
    return f"{city}天气：雨天"


"""
中间件可以打断（插入）的六个时间节点
1. agent 执行前
2. agent 执行后
3. model 执行前
4. model 执行后
5. 工具执行中
6. 模型执行中
"""

@before_agent
def log_before_agent(state:AgentState,runtime:Runtime):
    #agent执行前会调用这个函数并传入 state 和 runtime 两个对象
    #state: 完整的上下文信息    runtime: 携带的是本轮会话信息
    print(f"[before agent] agent启动，并附带{len(state["messages"])}条消息")

@after_agent
def log_after_agent(state:AgentState,runtime:Runtime):
    #agent执行后会调用这个函数并传入 state 和 runtime 两个对象
    #state: 完整的上下文信息    runtime: 携带的是本轮会话信息
    print(f"[after agent] agent结束，并附带{len(state["messages"])}条消息")

@before_model
def log_before_model(state:AgentState,runtime:Runtime):
    #agent执行前会调用这个函数并传入 state 和 runtime 两个对象
    #state: 完整的上下文信息    runtime: 携带的是本轮会话信息
    print(f"[before_model] 模型即将启动，并附带{len(state["messages"])}条消息")

@after_model
def log_after_model(state:AgentState,runtime:Runtime):
    #agent执行前会调用这个函数并传入 state 和 runtime 两个对象
    #state: 完整的上下文信息    runtime: 携带的是本轮会话信息
    print(f"[after_model] 模型调用结束，并附带{len(state["messages"])}条消息")

@wrap_model_call
def model_call_hook(request,handler):
    print("模型调用啦！")
    return handler(request)

@wrap_tool_call
def monitor_tool(request,handler):
    print(f"选用工具：{request.tool_call['name']}")
    print(f"工具传入参数：{request.tool_call['args']}")
    return handler(request)

agent = create_agent(
    model=ChatTongyi(model="qwen3-max"),
    tools=[get_weather],
    middleware=[model_call_hook, monitor_tool,log_before_agent,log_after_agent,log_before_model,log_after_model],
)

res = agent.invoke(
    {"messages":[{"role":"user","content":"深圳今天的天气如何，如何穿衣呢"}]}
)

print("****************************\n", res)