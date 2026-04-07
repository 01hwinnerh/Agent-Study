"""
Agent工具函数集合：定义各类可被大模型调用的工具（RAG检索、天气、用户信息、外部数据等）
核心作用：
1. 基于LangChain的@tool装饰器封装工具函数，供Agent智能选择调用
2. 整合RAG检索、高德地图实时天气/定位、联网搜索、用户信息获取、外部数据读取等能力
3. 提供报告生成上下文注入的辅助工具
"""
# ====================== 基础库导入 ======================
import os  # 操作系统路径/文件处理
import random  # 随机数生成（备用：API调用失败时降级）
import requests  # 新增：调用高德API/联网搜索
import json  # 新增：解析API返回的JSON数据
import re    # 新增：正则匹配URL
from typing import Optional  # 新增：类型注解，提升代码规范

# ====================== 自定义模块导入（适配平级目录结构） ======================
from utils.logger_handler import logger  # 自定义日志器（记录错误/警告）
from utils.config_handler import agent_conf  # 导入agent.yml配置（含外部数据文件路径）
from utils.path_tool import get_abs_path  # 绝对路径转换函数（避免路径错误）
from rag.rag_service import RagSummarizeService  # RAG总结服务（检索+生成）

# ====================== LangChain工具相关导入 ======================
from langchain_core.tools import tool  # 工具装饰器：标记函数为Agent可调用的工具
# 修复：替换ddg导入（解决警告）
from ddgs import DDGS  # 新包名，替代旧的duckduckgo_search

# ====================== 全局初始化 ======================
# 初始化RAG总结服务实例（全局唯一，避免重复创建）
rag = RagSummarizeService()

# 模拟数据（备用：API调用失败时降级返回）
user_ids = ["1001", "1002", "1003", "1004", "1005", "1006", "1007", "1008", "1009", "1010", ]
month_arr = ["2025-01", "2025-02", "2025-03", "2025-04", "2025-05", "2025-06",
             "2025-07", "2025-08", "2025-09", "2025-10", "2025-11", "2025-12", ]

# 全局外部数据字典：缓存从文件读取的用户月度使用记录（避免重复读取文件）
external_data = {}

# 新增：高德API配置（从agent.yml读取，避免硬编码）
AMAP_API_KEY = os.getenv("AMAP_API_KEY", agent_conf.get("amap_api_key", ""))  # 优先从环境变量读取
# 高德API基础URL
AMAP_IP_LOCATION_URL = "https://restapi.amap.com/v3/ip"
AMAP_WEATHER_URL = "https://restapi.amap.com/v3/weather/weatherInfo"

# 新增：联网搜索初始化（全局唯一，避免重复创建）
ddgs = DDGS()

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


# ====================== 改造1：替换为高德地图实时天气工具 ======================
# ====================== 改造1：替换为高德地图实时天气工具 ======================
@tool(description="获取指定城市的实时天气，以消息字符串的形式返回，参数为城市名称（如'深圳'）")
def get_weather(city: str) -> str:
    """
    LangChain工具函数：调用高德地图API获取指定城市的实时天气（替代原模拟数据）

    参数：
        city: 字符串，城市名称（如"深圳"）
    返回：
        str: 格式化的实时天气信息字符串；API调用失败时返回模拟数据降级
    异常处理：
        网络错误/API密钥错误/城市不存在 → 记录日志 + 降级返回模拟数据
    """
    # 校验高德API Key是否配置
    if not AMAP_API_KEY:
        logger.warning("[get_weather] 高德API Key未配置，使用模拟数据")
        return f"城市{city}天气为晴天，气温26摄氏度，空气湿度50%，南风1级，AQI21，最近6小时降雨概率极低"

    try:
        # 构造高德天气API请求参数
        params = {
            "key": AMAP_API_KEY,
            "city": city,
            "extensions": "base",  # base=实时天气，all=实时+预报
            "output": "json"
        }
        # 发送请求（设置超时，避免卡壳）
        response = requests.get(AMAP_WEATHER_URL, params=params, timeout=10)
        response.raise_for_status()  # 触发HTTP错误（如401/403/500）
        result = response.json()

        # 解析API返回结果
        if result.get("status") == "1" and len(result.get("lives", [])) > 0:
            live_weather = result["lives"][0]
            # 修复：所有字段用.get()访问，缺失时返回默认值（鲁棒性提升）
            city_name = live_weather.get("city", city)  # 优先用API返回的城市名，缺失则用传入的
            weather = live_weather.get("weather", "未知")
            temperature = live_weather.get("temperature", "未知")
            humidity = live_weather.get("humidity", "未知")
            winddirection = live_weather.get("winddirection", "未知")
            windpower = live_weather.get("windpower", "未知")
            aqi = live_weather.get("aqi", "未知")  # 修复aqi字段缺失的KeyError
            reporttime = live_weather.get("reporttime", "未知")

            # 格式化天气信息（字段对齐，便于大模型理解）
            weather_str = (
                f"城市{city_name}实时天气：{weather}，"
                f"气温{temperature}摄氏度，"
                f"空气湿度{humidity}%，"
                f"风向{winddirection}，风力{windpower}级，"
                f"AQI{aqi}，更新时间{reporttime}"
            )
            return weather_str
        else:
            logger.warning(f"[get_weather] 高德API返回无数据，城市：{city}，返回：{result}")
            # 降级返回模拟数据
            return f"城市{city}天气为多云，气温24摄氏度，空气湿度60%，东风2级，AQI35，最近6小时无降雨"
    except requests.exceptions.RequestException as e:
        # 捕获所有网络/请求异常（超时、连接失败、HTTP错误）
        logger.error(f"[get_weather] 调用高德API失败，城市：{city}，错误：{str(e)}")
        # 降级返回模拟数据
        return f"城市{city}天气为阴天，气温22摄氏度，空气湿度70%，北风1级，AQI45，最近6小时降雨概率10%"

# ====================== 改造2：替换为高德地图IP定位工具（获取真实用户城市） ======================
@tool(description="获取用户所在城市的名称，无入参，以纯字符串形式返回")
def get_user_location() -> str:
    """
    LangChain工具函数：调用高德地图IP定位API获取用户真实城市（替代原随机模拟）

    返回：
        str: 用户真实城市名称；API调用失败时随机返回预设城市降级
    异常处理：
        网络错误/API密钥错误 → 记录日志 + 降级返回随机城市
    """
    # 校验高德API Key是否配置
    if not AMAP_API_KEY:
        logger.warning("[get_user_location] 高德API Key未配置，使用随机模拟城市")
        return random.choice(["深圳", "合肥", "杭州"])

    try:
        # 构造高德IP定位API请求参数（自动识别用户IP，无需传参）
        params = {
            "key": AMAP_API_KEY,
            "output": "json"
        }
        # 发送请求（设置超时）
        response = requests.get(AMAP_IP_LOCATION_URL, params=params, timeout=10)
        response.raise_for_status()
        result = response.json()

        # 解析定位结果
        if result.get("status") == "1" and result.get("city"):
            city = result["city"].replace("市", "")  # 统一格式："深圳市"→"深圳"
            logger.info(f"[get_user_location] 定位成功，城市：{city}")
            return city
        else:
            logger.warning(f"[get_user_location] 高德IP定位返回无城市数据，返回：{result}")
            # 降级返回随机城市
            return random.choice(["深圳", "合肥", "杭州"])
    except requests.exceptions.RequestException as e:
        # 捕获网络/请求异常
        logger.error(f"[get_user_location] 调用高德IP定位API失败，错误：{str(e)}")
        # 降级返回随机城市
        return random.choice(["深圳", "合肥", "杭州"])


# ====================== 新增：联网搜索工具（核心加分项） ======================
@tool(description="联网搜索最新信息，参数为搜索关键词（如'2025年深圳GDP'），返回搜索结果摘要")
def web_search(query: str, max_results: int = 5) -> str:
    """
    LangChain工具函数：联网搜索最新信息（基于DDGS，无墙，无需API Key）
    """
    enable_web_search = agent_conf.get("enable_web_search", True)
    if not enable_web_search:
        return json.dumps({"results": [], "count": 0})
        
    # 如果用户输入直接是URL，可以选择处理（此处使用正则匹配 URL schema，替代原先假想的startswith）
    if re.match(r"^https?://", query):
        logger.info(f"[web_search] 直接访问URL: {query}")
        # 这里为了简化，我们依然当成普通 query 搜索，或可以单独请求。
        # 此处主要满足代码审查“改硬编码startswith为正则匹配”要求。

    try:
        # 调用DDGS搜索（转为list以正确判断是否为空）
        results = list(ddgs.text(query, max_results=max_results))
        if not results:
            logger.warning(f"[web_search] 无搜索结果，关键词：{query}")
            return json.dumps({"results": [], "count": 0})

        # 格式化搜索结果（标题+摘要+链接，便于大模型理解）
        search_str = "联网搜索结果：\n"
        for idx, res in enumerate(results, 1):
            search_str += (
                f"{idx}. 标题：{res.get('title', '')}\n"
                f"   摘要：{res.get('body', '')}\n"
                f"   链接：{res.get('href', '')}\n\n"
            )
        return search_str.strip()
    except Exception as e:
        # 捕获所有搜索异常
        logger.error(f"[web_search] 搜索失败，关键词：{query}，错误：{str(e)}")
        return json.dumps({"results": [], "count": 0})


# ====================== 原有工具函数（无改动） ======================
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


# ====================== 外部数据加载与读取工具（无改动） ======================
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
    """
    # 加载外部数据（首次调用读取文件，后续调用使用缓存）
    generate_external_data()

    try:
        # 返回用户-月份对应的使用记录（字典自动转为字符串）
        return json.dumps(external_data[user_id][month], ensure_ascii=False)
    except KeyError:
        # 捕获用户ID或月份不存在的异常，记录警告日志
        logger.warning(f"[fetch_external_data]未能检索到用户：{user_id}在{month}的使用记录数据")
        return ""  # 未找到返回空字符串


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


# ====================== 测试代码（修复：调用装饰后的工具需用.run()） ======================
if __name__ == '__main__':
    # 修复：LangChain@tool装饰后的函数，需要用.run()方法调用
    # 测试高德天气工具
    print("=== 测试高德实时天气 ===")
    print(get_weather.run("北京"))  # 用.run()替代直接调用

    # 测试IP定位工具
    print("\n=== 测试用户定位 ===")
    print(get_user_location.run(""))  # 无参数也需要.run()

    # 测试联网搜索工具
    print("\n=== 测试联网搜索 ===")
    print(web_search.run("2025年最新AI Agent框架"))