# 导入操作系统模块（路径处理）、哈希模块（计算MD5）
import os, hashlib
# 导入自定义日志器（已配置的logger，用于输出日志信息）
from utils.logger_handler import logger

# 导入LangChain核心文档类（统一文档格式）
from langchain_core.documents import Document
# 导入LangChain社区的文档加载器：PDF加载器、文本文件加载器
from langchain_community.document_loaders import PyPDFLoader, TextLoader


# ====================== 核心函数1：计算文件MD5值（用于文件唯一性校验） ======================
def get_file_md5_hex(filepath: str) -> str | None:
    """
    计算文件的MD5哈希值（十六进制字符串），用于校验文件是否被修改/重复

    参数：
        filepath: 待计算MD5的文件绝对/相对路径

    返回：
        str: 文件的MD5十六进制字符串（32位）；None: 计算失败（文件不存在/不是文件/读取错误）

    设计思路：
        1. 分片读取（4KB）：避免大文件一次性加载导致内存溢出
        2. 二进制读取：保证MD5计算的准确性（文本文件编码不影响结果）
        3. 完善日志：便于定位计算失败的原因
    """
    # 第一步：校验文件是否存在
    if not os.path.exists(filepath):
        logger.error(f"[MD5计算] 文件{filepath}不存在，无法计算MD5")
        return None  # 原代码无return，补充返回None，避免后续调用报AttributeError

    # 第二步：校验路径是否为文件（排除文件夹）
    if not os.path.isfile(filepath):
        logger.error(f"[MD5计算] 路径{filepath}不是文件，无法计算MD5")
        return None

    # 第三步：初始化MD5对象
    md5_obj = hashlib.md5()
    chunk_size = 4096  # 4KB分片读取，平衡性能和内存占用（大文件推荐16KB/32KB）

    try:
        # 以二进制模式打开文件（rb）：MD5计算必须基于字节流，避免文本编码干扰
        with open(filepath, "rb") as f:
            # 循环分片读取文件：chunk := f.read(chunk_size) 是海象运算符（Python3.8+），读取到末尾返回空字节串
            while chunk := f.read(chunk_size):
                md5_obj.update(chunk)  # 更新MD5对象（累加计算分片哈希）

        # 生成32位十六进制MD5字符串
        md5_hex = md5_obj.hexdigest()
        logger.info(f"[MD5计算] 文件{filepath}的MD5值：{md5_hex}")
        return md5_hex

    except Exception as e:
        # 捕获所有异常（文件权限不足、文件损坏、读取中断等）
        logger.error(f"[MD5计算] 计算文件{filepath}的MD5失败，错误信息：{str(e)}")
        return None


# ====================== 核心函数2：筛选指定类型的文件列表 ======================
def listdir_with_allowed_type(path: str, allowed_types: tuple[str]) -> tuple[str]:
    """
    遍历指定文件夹，返回符合允许后缀的文件路径列表（绝对/相对路径）

    参数：
        path: 待遍历的文件夹路径
        allowed_types: 允许的文件后缀元组（如(".pdf", ".txt")）

    返回：
        tuple[str]: 符合条件的文件路径元组；空元组：文件夹不存在/无符合条件的文件

    修复点：
        原代码错误返回allowed_types，现改为返回空元组，符合函数语义
    """
    files = []  # 初始化符合条件的文件列表

    # 校验路径是否为文件夹
    if not os.path.isdir(path):
        logger.error(f"[文件筛选] 路径{path}不是文件夹，无法遍历")
        return tuple(files)  # 原代码返回allowed_types，逻辑错误，改为返回空元组

    # 遍历文件夹内的所有文件/子文件夹
    for f in os.listdir(path):
        # 拼接完整路径（避免相对路径问题）
        full_path = os.path.join(path, f)
        # 仅筛选文件（排除子文件夹）+ 后缀符合允许类型
        if os.path.isfile(full_path) and f.endswith(allowed_types):
            files.append(full_path)
            logger.debug(f"[文件筛选] 匹配文件：{full_path}")

    # 转换为元组（不可变，避免后续意外修改）
    return tuple(files)


# ====================== 核心函数3：PDF文件加载器（转换为LangChain Document对象） ======================
def pdf_loader(filepath: str, passwd: str | None = None) -> list[Document]:
    """
    加载PDF文件，转换为LangChain的Document对象列表（每页对应一个Document）

    参数：
        filepath: PDF文件路径
        passwd: PDF密码（可选，加密PDF需传入）

    返回：
        list[Document]: 包含PDF内容的Document列表；空列表：加载失败
    """
    try:
        # 初始化PDF加载器（支持加密PDF）
        loader = PyPDFLoader(filepath, password=passwd)
        # 加载PDF并转换为Document列表：每个Document包含page_content（内容）、metadata（元数据：页码、路径等）
        docs = loader.load()
        logger.info(f"[PDF加载] 成功加载{filepath}，共{len(docs)}页")
        return docs

    except Exception as e:
        logger.error(f"[PDF加载] 加载{filepath}失败，错误信息：{str(e)}")
        return []  # 原代码无异常处理，补充返回空列表，避免程序崩溃


# ====================== 核心函数4：TXT文件加载器（转换为LangChain Document对象） ======================
def txt_loader(filepath: str) -> list[Document]:
    """
    加载TXT文本文件，转换为LangChain的Document对象列表（整个文件对应一个Document）

    参数：
        filepath: TXT文件路径

    返回：
        list[Document]: 包含TXT内容的Document列表；空列表：加载失败
    """
    try:
        # 初始化TXT加载器，指定编码为utf-8（避免中文乱码）
        loader = TextLoader(filepath, encoding="utf-8")
        # 加载TXT并转换为Document列表：仅1个Document，包含全部内容
        docs = loader.load()
        logger.info(f"[TXT加载] 成功加载{filepath}，内容长度：{len(docs[0].page_content) if docs else 0}字符")
        return docs

    except Exception as e:
        logger.error(f"[TXT加载] 加载{filepath}失败，错误信息：{str(e)}")
        return []  # 原代码无异常处理，补充返回空列表