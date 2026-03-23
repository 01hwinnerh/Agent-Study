"""
Agent工具函数集合：定义各类可被大模型调用的工具（RAG检索、天气、用户信息、外部数据等）
核心作用：
1. 基于LangChain的@tool装饰器封装工具函数，供Agent智能选择调用
2. 整合RAG检索、模拟天气查询、用户信息获取、外部数据读取等能力
3. 提供报告生成上下文注入的辅助工具
"""
# ====================== 基础库导入 ======================
import os  # 操作系统路径/文件处理
import random  # 随机数生成（模拟用户位置/ID/月份）

# ====================== 自定义模块导入（适配平级目录结构） ======================
from utils.logger_handler import logger  # 自定义日志器（记录错误/警告）
from utils.config_handler import agent_conf  # 导入agent.yml配置（含外部数据文件路径）
from utils.path_tool import get_abs_path  # 绝对路径转换函数（避免路径错误）
from rag.rag_service import RagSummarizeService  # RAG总结服务（检索+生成）

# ====================== LangChain工具相关导入 ======================
from langchain_core.tools import tool  # 工具装饰器：标记函数为Agent可调用的工具

# ====================== 全局初始化 ======================
# 初始化RAG总结服务实例（全局唯一，避免重复创建）
rag = RagSummarizeService()

# 模拟用户ID列表（用于get_user_id工具随机返回）
user_ids = ["1001", "1002", "1003", "1004", "1005", "1006", "1007", "1008", "1009", "1010", ]
# 模拟月份列表（用于get_current_month工具随机返回）
month_arr = ["2025-01", "2025-02", "2025-03", "2025-04", "2025-05", "2025-06",
             "2025-07", "2025-08", "2025-09", "2025-10", "2025-11", "2025-12", ]

# 全局外部数据字典：缓存从文件读取的用户月度使用记录（避免重复读取文件）
external_data = {}


# ====================== LangChain工具函数定义 ======================
@tool(description="从向量存储中检索参考资料")
def rag_summarize(query: str) -> str:
    """
    LangChain工具函数：调用RAG总结服务，检索与提问相关的参考资料并生成总结

    参数：
        query: 字符串，用户的提问内容（如"小户型适合哪些扫地机器人"）
    返回：
        str: 基于向量库检索结果生成的总结回复
    """
    return rag.rag_summarize(query)


@tool(description="获取指定城市的天气，以消息字符串的形式返回")
def get_weather(city: str) -> str:
    """
    LangChain工具函数：模拟获取指定城市的天气信息（固定返回测试数据）

    参数：
        city: 字符串，城市名称（如"深圳"）
    返回：
        str: 格式化的天气信息字符串（模拟数据，无真实调用天气API）
    """
    return f"城市{city}天气为晴天，气温26摄氏度，空气湿度50%，南风1级，AQI21，最近6小时降雨概率极低"


@tool(description="获取用户所在城市的名称，以纯字符串形式返回")
def get_user_location() -> str:
    """
    LangChain工具函数：随机返回预设城市列表中的一个（模拟获取用户定位）

    返回：
        str: 随机城市名称（深圳/合肥/杭州）
    """
    return random.choice(["深圳", "合肥", "杭州"])


@tool(description="获取用户的ID，以纯字符串形式返回")
def get_user_id() -> str:
    """
    LangChain工具函数：随机返回预设用户ID列表中的一个（模拟获取用户ID）

    返回：
        str: 随机用户ID（如"1001"）
    """
    return random.choice(user_ids)


@tool(description="获取当前月份，以纯字符串形式返回")
def get_current_month() -> str:
    """
    LangChain工具函数：随机返回预设月份列表中的一个（模拟获取当前月份）

    返回：
        str: 随机月份（如"2025-01"）
    """
    return random.choice(month_arr)


# ====================== 外部数据加载与读取工具 ======================
def generate_external_data():
    """
    加载外部数据文件（CSV格式）到全局external_data字典，格式如下：
    {
        "user_id": {
            "month" : {"特征": xxx, "效率": xxx, "耗材": xxx, "对比": xxx},
            "month" : {"特征": xxx, "效率": xxx, "耗材": xxx, "对比": xxx},
            ...
        },
        ...
    }
    核心逻辑：
    1. 仅在external_data为空时加载（避免重复读取文件）
    2. 读取CSV文件，跳过首行（表头），按逗号分割每行数据
    3. 解析用户ID/特征/效率/耗材/对比/月份，构建嵌套字典

    异常：
        FileNotFoundError: 外部数据文件不存在时抛出
    :return: None（数据存入全局external_data字典）
    """
    # 仅当external_data为空时加载（缓存机制，避免重复IO）
    if not external_data:
        # 从配置中获取外部数据文件路径，转换为绝对路径
        external_data_path = get_abs_path(agent_conf["external_data_path"])

        # 检查文件是否存在，不存在则抛出异常
        if not os.path.exists(external_data_path):
            raise FileNotFoundError(f"外部数据文件{external_data_path}不存在")

        # 读取文件并解析每行数据
        with open(external_data_path, "r", encoding="utf-8") as f:
            # 跳过首行（表头），遍历剩余行
            for line in f.readlines()[1:]:
                # 去除首尾空白，按逗号分割为列表
                arr: list[str] = line.strip().split(",")

                # 解析每行数据（去除字符串中的双引号，避免格式干扰）
                user_id: str = arr[0].replace('"', "")  # 第1列：用户ID
                feature: str = arr[1].replace('"', "")  # 第2列：特征
                efficiency: str = arr[2].replace('"', "")  # 第3列：效率
                consumables: str = arr[3].replace('"', "")  # 第4列：耗材
                comparison: str = arr[4].replace('"', "")  # 第5列：对比
                time: str = arr[5].replace('"', "")  # 第6列：月份

                # 初始化用户ID对应的字典（首次出现时）
                if user_id not in external_data:
                    external_data[user_id] = {}

                # 构建用户-月份-数据的嵌套结构
                external_data[user_id][time] = {
                    "特征": feature,
                    "效率": efficiency,
                    "耗材": consumables,
                    "对比": comparison,
                }


@tool(description="从外部系统中获取指定用户在指定月份的使用记录，以纯字符串形式返回， 如果未检索到返回空字符串")
def fetch_external_data(user_id: str, month: str) -> str:
    """
    LangChain工具函数：获取指定用户在指定月份的使用记录

    参数：
        user_id: 字符串，用户ID（如"1001"）
        month: 字符串，月份（如"2025-01"）
    返回：
        str: 该用户该月份的使用记录字典（转为字符串）；未找到则返回空字符串
    流程：
        1. 调用generate_external_data加载数据（首次调用时读取文件，后续调用使用缓存）
        2. 尝试从external_data中读取数据，捕获KeyError（用户/月份不存在）
        3. 未找到时记录警告日志，返回空字符串
    """
    # 加载外部数据（首次调用读取文件，后续调用使用缓存）
    generate_external_data()

    try:
        # 返回用户-月份对应的使用记录（字典自动转为字符串）
        return external_data[user_id][month]
    except KeyError:
        # 捕获用户ID或月份不存在的异常，记录警告日志
        logger.warning(f"[fetch_external_data]未能检索到用户：{user_id}在{month}的使用记录数据")
        return ""  # 未找到返回空字符串


# 测试代码（注释状态）：验证fetch_external_data工具
# if __name__ =='__main__':
#    print=(fetch_external_data("1001","2025-01"))

@tool(
    description="无入参，无返回值，调用后触发中间件自动为报告生成的场景动态注入上下文信息，为后续提示词切换提供上下文信息")
def fill_context_for_report():
    """
    LangChain工具函数：触发报告生成的上下文注入（模拟实现）

    作用：
        告知中间件为报告生成场景注入上下文，便于后续提示词根据上下文切换内容
    返回：
        str: 固定提示字符串（模拟调用成功的反馈）
    """
    return "fill_context_for_report已调用"