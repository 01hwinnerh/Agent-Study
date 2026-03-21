"""
功能：大模型/嵌入模型工厂类（基于工厂模式封装）
核心作用：
1. 统一创建通义千问对话模型（ChatTongyi）和嵌入模型（DashScopeEmbeddings）
2. 基于配置文件（rag_conf）动态指定模型名称，便于灵活切换
3. 采用抽象基类（ABC）定义统一接口，符合面向对象设计原则

适配目录结构：
- 当前文件（factory.py）位于 model/ 文件夹
- utils/ 文件夹与 model/ 平级，导入时直接使用 from utils.xxx import xxx
- 需确保 AI大模型_Agent项目/ 被标记为 PyCharm Sources Root
"""
# ====================== 基础库/类型导入 ======================
from abc import ABC, abstractmethod  # 抽象基类相关：定义接口规范
from typing import Optional  # 类型注解：标记可选返回值

# ====================== LangChain 模型相关导入 ======================
# LangChain 核心嵌入模型抽象类：所有嵌入模型需实现该接口
from langchain_core.embeddings import Embeddings
# 通义千问对话模型基类：约束对话模型的统一接口
from langchain_community.chat_models.tongyi import BaseChatModel
# 通义千问嵌入模型：用于将文本转为向量（适配Chroma向量库）
from langchain_community.embeddings import DashScopeEmbeddings
# 通义千问对话模型：用于生成自然语言回答（Agent核心）
from langchain_community.chat_models.tongyi import ChatTongyi

# ====================== 自定义配置导入（适配平级目录） ======================
# 说明：utils/ 与 model/ 平级，需确保 AI大模型_Agent项目/ 为 Sources Root
from utils.config_handler import rag_conf  # 导入rag.yml配置（含模型名称）


# ====================== 抽象基类：定义模型创建统一接口 ======================
class BaseModelFactory(ABC):
    """
    模型工厂抽象基类（核心接口）
    作用：定义所有模型工厂必须实现的 generator 方法，强制子类遵循统一规范
    设计模式：工厂模式 + 抽象接口，便于扩展新模型（如添加OpenAI模型工厂）
    """

    @abstractmethod  # 抽象方法：子类必须实现，否则实例化会报错
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        """
        生成模型实例的统一接口

        返回值：
            Optional[Embeddings | BaseChatModel]:
            - Embeddings：嵌入模型实例（如DashScopeEmbeddings）
            - BaseChatModel：对话模型实例（如ChatTongyi）
            - None：模型创建失败时返回（当前代码未处理失败场景）
        """
        pass  # 抽象方法无实现，仅定义接口


# ====================== 对话模型工厂：创建ChatTongyi实例 ======================
class ChatModelFactory(BaseModelFactory):
    """
    对话模型工厂类（具体实现）
    作用：创建通义千问对话模型（ChatTongyi）实例
    依赖：rag_conf["chat_model_name"] 配置项（如"qwen3-max"）
    """

    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        """
        生成通义千问对话模型实例

        返回：
            ChatTongyi实例（继承自BaseChatModel）：可直接用于Agent对话生成
        配置依赖：
            rag_conf["chat_model_name"]：在rag.yml中配置的对话模型名称，如"qwen-turbo"、"qwen3-max"
        """
        # 从配置中读取模型名称，动态创建对话模型
        # ChatTongyi初始化参数说明：
        # - model：模型名称（必填）
        # - api_key：通义千问API密钥（可选，若未传则读取环境变量DASHSCOPE_API_KEY）
        return ChatTongyi(model=rag_conf["chat_model_name"])


# ====================== 嵌入模型工厂：创建DashScopeEmbeddings实例 ======================
class EmbeddingsFactory(BaseModelFactory):
    """
    嵌入模型工厂类（具体实现）
    作用：创建通义千问嵌入模型（DashScopeEmbeddings）实例
    依赖：rag_conf["embedding_model_name"] 配置项（如"text-embedding-v3"）
    """

    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        """
        生成通义千问嵌入模型实例

        返回：
            DashScopeEmbeddings实例（继承自Embeddings）：可用于Chroma向量库的文本嵌入
        配置依赖：
            rag_conf["embedding_model_name"]：在rag.yml中配置的嵌入模型名称，如"text-embedding-v1"
        """
        # 从配置中读取模型名称，动态创建嵌入模型
        # DashScopeEmbeddings初始化参数说明：
        # - model：嵌入模型名称（必填）
        # - api_key：通义千问API密钥（可选，读取环境变量DASHSCOPE_API_KEY）
        return DashScopeEmbeddings(model=rag_conf["embedding_model_name"])


# ====================== 全局模型实例化（供其他模块直接导入使用） ======================
# 创建对话模型实例：其他模块可直接 from model.factory import chat_model 使用
chat_model = ChatModelFactory().generator()

# 创建嵌入模型实例：其他模块可直接 from model.factory import embed_model 使用
# （如VectorStoreService中用于Chroma向量库的embedding_function）
embed_model = EmbeddingsFactory().generator()