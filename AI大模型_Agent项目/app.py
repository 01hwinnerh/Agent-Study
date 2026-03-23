import time

import streamlit as st
from agent.react_agent import ReactAgent

# 设置页面标题（显示在浏览器标签和页面顶部）
st.title("智扫通机器人智能客服")
# 添加一条水平分割线，用于视觉分隔
st.divider()

# 检查 session_state 中是否已初始化 agent 实例
# 如果没有，则创建一个 ReactAgent 对象并存入会话状态（避免每次刷新都重建）
if "agent" not in st.session_state:
    st.session_state["agent"] = ReactAgent()

# 检查 session_state 中是否已有聊天消息历史
# 如果没有，则初始化为空列表
if "message" not in st.session_state:
    st.session_state["message"] = []

# 遍历当前会话中的所有历史消息，并在界面上逐条显示
for message in st.session_state["message"]:
    # 根据消息角色（user/assistant）显示不同样式的聊天气泡
    st.chat_message(message["role"]).write(message["content"])

# 显示聊天输入框，用户输入后返回内容（若未输入则为 None）
prompt = st.chat_input()

# 当用户输入了内容（即 prompt 不为 None 且非空）
if prompt:
    # 在界面上显示用户的输入消息（左侧气泡）
    st.chat_message("user").write(prompt)
    # 将用户消息追加到会话历史中
    st.session_state["message"].append({"role": "user", "content": prompt})

    # 用于临时缓存 Agent 流式返回的所有 chunk（最终取最后一个作为完整回答）
    response_messages = []

    # 显示“思考中...”加载动画
    with st.spinner("智能客服思考中..."):
        # 调用 Agent 的流式执行方法，获取生成器对象（逐步返回回答片段）
        res_stream = st.session_state["agent"].execute_stream(prompt)


        # 定义一个内部函数：用于捕获流式输出的每个 chunk，并逐字符模拟打字效果
        def capture(generator, cache_list):  # 捕获
            # 遍历生成器返回的每一个文本块（chunk）
            for chunk in generator:
                # 将当前 chunk 存入缓存列表（用于后续保存完整回答）
                cache_list.append(chunk)

                # 对 chunk 中的每个字符逐个 yield，配合 time.sleep 实现打字机效果
                for char in chunk:
                    time.sleep(0.01)  # 每个字符间隔 0.01 秒，模拟人工输入
                    yield char  # 返回单个字符给 write_stream


        # 使用 Streamlit 的流式写入功能，实时显示 AI 回答（右侧气泡）
        st.chat_message("assistant").write_stream(capture(res_stream, response_messages))

        # 将 AI 的完整回答（取缓存列表最后一个 chunk，通常为最终完整回复）存入历史
        st.session_state["message"].append({"role": "assistant", "content": response_messages[-1]})

        # 强制重新运行整个脚本（刷新页面状态，确保新消息立即显示且输入框清空）
        st.rerun()