"""
功能：向量库服务类（VectorStoreService）
核心作用：
1. 初始化Chroma向量库（配置嵌入模型、存储路径、分块规则）
2. 加载指定目录下的PDF/TXT文件，分块后存入向量库
3. 基于文件MD5实现去重，避免重复加载相同文件
4. 提供向量检索器（retriever）供RAG流程调用

适配目录结构：所有utils/下的文件均为平级，导入时无需加utils.前缀
"""
# ====================== 基础库导入 ======================
import os  # 操作系统路径/文件处理
# LangChain Chroma向量库核心类：用于创建/操作向量库
from langchain_chroma import Chroma
# LangChain核心文档类：统一文档格式（page_content+metadata）
from langchain_core.documents import Document
# 文本分块器：按规则将长文档切分为小片段（适配向量嵌入）
from langchain_text_splitters import RecursiveCharacterTextSplitter

# ====================== 自定义模块导入（适配同目录结构） ======================
# 说明：所有文件在utils/文件夹下，直接导入同目录的兄弟文件，无需加utils.前缀
from utils.config_handler import chroma_conf  # 导入Chroma向量库配置（chroma.yml解析结果）
from model.factory import embed_model  # 导入嵌入模型实例（如通义千问/OpenAI嵌入模型）
from utils.path_tool import get_abs_path  # 导入绝对路径转换函数
from utils.file_handler import (  # 导入文件处理工具函数
    pdf_loader,  # PDF文件加载为Document列表
    txt_loader,  # TXT文件加载为Document列表
    listdir_with_allowed_type,  # 筛选指定类型的文件
    get_file_md5_hex  # 计算文件MD5值（去重核心）
)
from utils.logger_handler import logger  # 导入自定义日志器


# ====================== 向量库服务核心类 ======================
class VectorStoreService:
    def __init__(self):
        """
        初始化向量库服务
        1. 创建Chroma向量库实例（绑定嵌入模型、存储目录、集合名）
        2. 初始化文本分块器（按chroma.yml配置的分块规则）
        """
        # 1. 初始化Chroma向量库
        self.vector_store = Chroma(
            collection_name=chroma_conf["collection_name"],  # 向量库集合名（如"rag_knowledge"）
            embedding_function=embed_model,  # 嵌入模型（将文本转为向量）
            persist_directory=chroma_conf["persist_directory"],  # 向量库本地存储路径（如"chroma_db"）
        )

        # 2. 初始化文本分块器（RecursiveCharacterTextSplitter：递归字符分块，优先按分隔符切分）
        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=chroma_conf["chunk_size"],  # 分块大小（如500字符/块）
            chunk_overlap=chroma_conf["chunk_overlap"],  # 块重叠长度（如50字符，避免上下文断裂）
            separators=chroma_conf["separators"],  # 分隔符列表（如["\n\n", "\n", "。", "！", "？"]）
            length_function=len,  # 长度计算函数（按字符数计算）
        )

    def get_retriever(self):
        """
        获取向量检索器（供RAG流程调用，用于检索相关文档）

        返回：
            Retriever实例：基于Chroma的检索器，按top-k返回最相关的文档
        """
        # search_kwargs={"k": chroma_conf["k"]}：检索时返回前k个最相似的文档（如k=5）
        return self.vector_store.as_retriever(search_kwargs={"k": chroma_conf["k"]})

    def load_document(self):
        """
        核心功能：加载指定目录下的PDF/TXT文件，分块后存入向量库
        关键逻辑：
        1. 筛选指定类型的文件（PDF/TXT）
        2. 计算文件MD5，检查是否已加载（去重）
        3. 加载文件为Document对象 → 分块 → 存入向量库
        4. 记录已加载文件的MD5，避免重复处理
        :return: None
        """

        # ---------------- 内部辅助函数1：检查文件MD5是否已处理（去重核心） ----------------
        def check_md5_hex(md5_for_check: str):
            """
            检查文件MD5是否已存在于MD5记录文件中（判断是否已加载过）

            参数：
                md5_for_check: 待检查的文件MD5十六进制字符串
            返回：
                bool: True（已处理/已加载），False（未处理/未加载）
            """
            # 获取MD5记录文件的绝对路径
            md5_store_path = get_abs_path(chroma_conf["md5_hex_store"])

            # 如果MD5记录文件不存在，创建空文件并返回False（首次加载）
            if not os.path.exists(md5_store_path):
                open(md5_store_path, "w", encoding="utf-8").close()
                return False  # MD5未处理过

            # 读取MD5记录文件，逐行匹配
            with open(md5_store_path, "r", encoding="utf-8") as f:
                for line in f.readlines():
                    line = line.strip()  # 去除换行符/空格
                    if line == md5_for_check:
                        return True  # MD5已存在（文件已加载）
                return False  # MD5不存在（文件未加载）

        # ---------------- 内部辅助函数2：保存已处理文件的MD5（去重核心） ----------------
        def save_md5_hex(md5_for_check: str):
            """
            将已加载文件的MD5写入记录文件（追加模式）

            参数：
                md5_for_check: 已处理文件的MD5十六进制字符串
            """
            md5_store_path = get_abs_path(chroma_conf["md5_hex_store"])
            # 以追加模式写入（a），避免覆盖已有记录
            with open(md5_store_path, "a", encoding="utf-8") as f:
                f.write(md5_for_check + "\n")

        # ---------------- 内部辅助函数3：加载文件为Document列表 ----------------
        def get_file_documents(read_path: str):
            """
            根据文件后缀加载为LangChain Document列表

            参数：
                read_path: 文件绝对路径
            返回：
                list[Document]: 加载后的Document列表（空列表=加载失败/无内容）
            """
            if read_path.endswith("txt"):
                return txt_loader(read_path)  # 加载TXT文件
            if read_path.endswith("pdf"):
                return pdf_loader(read_path)  # 加载PDF文件
            return []  # 非PDF/TXT文件，返回空列表

        # ====================== 核心执行流程 ======================
        # 1. 筛选数据目录下允许的文件（PDF/TXT）
        allowed_files_path: list[str] = listdir_with_allowed_type(
            get_abs_path(chroma_conf["data_path"]),  # 数据目录绝对路径（如"docs/knowledge"）
            tuple(chroma_conf["allow_knowledge_file_type"]),  # 允许的文件类型（如(".pdf", ".txt")）
        )

        # 2. 遍历所有符合条件的文件，逐个处理
        for path in allowed_files_path:
            # 步骤1：计算文件MD5（用于去重）
            md5_hex = get_file_md5_hex(path)

            # 步骤2：检查MD5是否已处理，已处理则跳过
            if check_md5_hex(md5_hex):
                logger.info(f"[加载知识库]{path}内容已经存在知识库内，跳过")
                continue

            try:
                # 步骤3：加载文件为Document列表
                documents: list[Document] = get_file_documents(path)

                # 校验：文件无有效文本内容，跳过
                if not documents:
                    logger.warning(f"[加载知识库]{path}内没有有效文本内容，跳过")
                    continue

                # 步骤4：对Document进行分块（适配向量嵌入的长度限制）
                split_document: list[Document] = self.spliter.split_documents(documents)

                # 校验：分块后无有效内容，跳过
                if not split_document:
                    logger.warning(f"[加载知识库]{path}分片后没有有效文本内容，跳过")
                    continue

                # 步骤5：将分块后的Document存入向量库
                self.vector_store.add_documents(split_document)

                # 步骤6：保存MD5到记录文件，避免重复加载
                save_md5_hex(md5_hex)

                # 日志记录：加载成功
                logger.info(f"[加载知识库]{path} 内容加载成功")

            except Exception as e:
                # 捕获所有异常（文件损坏/嵌入失败/权限不足等），记录详细堆栈
                # exc_info=True：记录完整的异常堆栈，便于定位问题
                logger.error(f"[加载知识库]{path}加载失败：{str(e)}", exc_info=True)
                continue  # 跳过当前文件，继续处理下一个


# ====================== 测试代码 ======================
if __name__ == '__main__':
    # 1. 初始化向量库服务
    vs = VectorStoreService()

    # 2. 加载指定目录下的文件到向量库（自动去重）
    vs.load_document()

    # 3. 获取检索器（用于查询相关文档）
    retriever = vs.get_retriever()

    # 4. 测试检索：查询"迷路"相关的文档片段
    res = retriever.invoke("迷路")
    # 遍历检索结果，打印内容和分隔线
    for r in res:
        print(r.page_content)  # 打印文档片段内容
        print("-" * 20)  # 分隔线，便于阅读