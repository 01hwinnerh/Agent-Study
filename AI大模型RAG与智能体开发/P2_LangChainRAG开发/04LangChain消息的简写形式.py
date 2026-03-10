#langchain_community
from langchain_community.chat_models.tongyi import ChatTongyi

#获取聊天模型对象
model = ChatTongyi(model="qwen3-max")

#准备消息列表，简写形式是动态的，能够支持内部填充变量占位（后续的提示词模板时会用到，messages不支持变量占位哦）
messages = [
    ("system","你是一个边塞诗人"),
    ("human","写一首唐诗"),
    ("ai","锄禾日当午，汗滴禾下土，谁知盘中餐，粒粒皆辛苦。"),
    ("human","按照你上一个回复的格式，再写一首唐诗")
]



#调用stream流式执行
res = model.stream(input=messages)

#注意用.content来获取内容
for chunk in res:
    print(chunk.content,end="",flush=True)
