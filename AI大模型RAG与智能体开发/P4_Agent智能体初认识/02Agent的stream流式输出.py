from langchain.agents import create_agent
from langchain_community.chat_models import ChatTongyi
from langchain_core.tools import tool


@tool(description="传入股票名称，得到股价")
def get_price(name:str) -> str:
    return f"股票{name}的股价是3000元"

@tool(description="传入股票名称，得到公司相关信息")
def get_info(name:str) -> str:
    return f"股票{name}，是一家A股上市公司，市值3000亿"

agent = create_agent(
    model=ChatTongyi(model="qwen3-max"),
    tools=[get_price,get_info],
    system_prompt="你是一个智能助手，可以回答股票相关问题，请告知我思考过程，并且让我知道你为什么要调用某个工具",
)

for chunk in agent.stream(
    {"messages": [{"role": "user", "content": "传智教育股价多少，并且介绍一下"}]},
    stream_mode="values"
):
    #每个块都包含当前时刻完整状态，所以每次都要取最后一块
    latest_message = chunk["messages"][-1]
    # print(latest_message)

    if latest_message.content:
        print(type(latest_message).__name__,latest_message.content)

    try:
        if latest_message.tool_calls:
            print(f"工具调用：{[tc["name"] for tc in latest_message.tool_calls]}")
    except AttributeError as e:
        pass
