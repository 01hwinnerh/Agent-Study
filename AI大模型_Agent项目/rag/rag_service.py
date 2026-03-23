"""
总结服务类：用户提问，搜索参考资料，将提问和参考资料提交给模型，让模型总结回复
核心流程：
1. 初始化向量库检索器 → 2. 检索用户问题相关的参考文档 → 3. 拼接参考文档到提示词模板 → 4. 调用大模型生成总结回复
"""
# ====================== 基础库/类型导入 ======================
# LangChain核心文档类：表示检索到的参考文档（包含内容+元数据）
from langchain_core.documents import Document
# LangChain输出解析器：将模型输出（BaseMessage）转换为纯字符串
from langchain_core.output_parsers import StrOutputParser

# ====================== 自定义模块导入（适配平级目录结构） ======================
# 向量库服务类：用于初始化Chroma向量库、获取检索器、加载文档
from rag.vector_store import VectorStoreService
# 提示词加载工具：加载RAG专用提示词模板（从prompts.yml配置的文件中读取）
from utils.prompt_loader import load_rag_prompts
# LangChain提示词模板类：将字符串模板转为可动态填充参数的PromptTemplate
from langchain_core.prompts import PromptTemplate
# 大模型实例：导入预初始化的通义千问对话模型（ChatTongyi）
from model.factory import chat_model


# ====================== 辅助函数：打印提示词（调试用） ======================
def print_prompt(prompt):
    """
    辅助函数：打印拼接后的完整提示词（用于调试，查看最终传给模型的内容）

    参数：
        prompt: PromptTemplate实例/已填充参数的PromptValue
    返回：
        prompt: 原样返回输入的prompt，不影响链式调用
    """
    print("=" * 20)  # 分隔线，便于区分提示词内容
    print(prompt.to_string())  # 将prompt转为字符串并打印
    print("=" * 20)
    return prompt  # 返回原prompt，保证链式调用不中断


# ====================== RAG总结服务核心类 ======================
class RagSummarizeService(object):
    """
    RAG（检索增强生成）总结服务类
    核心功能：接收用户提问，检索相关参考文档，拼接提示词后调用大模型生成总结回复
    """

    def __init__(self):
        """
        初始化RAG总结服务
        步骤：
        1. 初始化向量库服务 → 2. 获取文档检索器 → 3. 加载RAG提示词模板 → 4. 初始化大模型 → 5. 构建链式调用流程
        """
        # 1. 初始化向量库服务（自动加载Chroma配置，绑定嵌入模型）
        self.vector_store = VectorStoreService()
        # 2. 获取向量库检索器（按chroma.yml配置的top-k检索相似文档）
        self.retriever = self.vector_store.get_retriever()
        # 3. 加载RAG提示词模板文本（从prompts.yml配置的rag_summarize_prompt_path文件读取）
        self.prompt_text = load_rag_prompts()
        # 4. 将提示词文本转为PromptTemplate（支持动态填充input/context参数）
        self.prompt_template = PromptTemplate.from_template(self.prompt_text)
        # 5. 绑定预初始化的大模型实例（通义千问ChatTongyi）
        self.model = chat_model
        # 6. 初始化链式调用流程（提示词填充 → 打印 → 模型调用 → 输出解析）
        self.chain = self._init_chain()

    def _init_chain(self):
        """
        初始化LangChain链式调用流程（私有方法，仅内部调用）
        链式流程说明（| 是LangChain的链式运算符）：
        PromptTemplate → print_prompt（调试打印） → chat_model（大模型） → StrOutputParser（解析为字符串）
        返回：
            Runnable序列：可直接调用invoke方法执行完整流程
        """
        # 构建链式调用：
        # 1. prompt_template：填充input/context参数生成完整提示词
        # 2. print_prompt：打印完整提示词（调试用，不影响流程）
        # 3. self.model：调用大模型生成回答
        # 4. StrOutputParser()：将模型返回的BaseMessage转为纯字符串
        chain = self.prompt_template | print_prompt | self.model | StrOutputParser()
        return chain

    def retriever_docs(self, query: str) -> list[Document]:
        """
        检索与用户提问相关的参考文档

        参数：
            query: 用户的提问字符串（如"小户型适合哪些扫地机器人"）
        返回：
            list[Document]: 检索到的相关文档列表（每个Document包含page_content和metadata）
        """
        # 调用检索器的invoke方法，传入用户提问，返回相似文档列表

        return self.retriever.invoke(query)

    def rag_summarize(self, query: str) -> str:
        """
        核心方法：执行RAG总结流程，生成最终回复

        参数：
            query: 用户的提问字符串
        返回：
            str: 大模型基于参考文档生成的总结回复
        """

        # 步骤1：检索与提问相关的参考文档
        context_docs = self.retriever_docs(query)

        # 步骤2：拼接参考文档为格式化的上下文字符串
        context = ""
        counter = 0  # 参考资料序号计数器
        for doc in context_docs:
            counter += 1
            # 拼接格式：【参考资料N】+ 文档内容 + 元数据（如来源文件、页码）
            context += f"【参考资料{counter}】: 参考资料：{doc.page_content} | 参考元数据：{doc.metadata}\n"

        # 步骤3：执行链式调用，传入参数（input=用户提问，context=拼接的参考文档）
        # invoke方法会自动执行：提示词填充 → 打印 → 模型调用 → 解析为字符串
        return self.chain.invoke(
            {
                "input": query,  # 绑定提示词模板中的{input}变量
                "context": context,  # 绑定提示词模板中的{context}变量
            }
        )


# ====================== 测试代码 ======================
if __name__ == '__main__':
    # 1. 初始化RAG总结服务实例
    rag = RagSummarizeService()

    # 2. 调用rag_summarize方法，传入测试问题，打印总结回复
    print(rag.rag_summarize("小户型适合哪些扫地机器人"))