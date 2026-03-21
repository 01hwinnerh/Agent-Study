"""
功能：加载不同类型的提示词模板文件（系统提示词、RAG提示词、报告生成提示词）
适配目录结构：所有文件均在 utils/ 文件夹下（平级），无需加 utils. 前缀导入
核心逻辑：
1. 从 prompts_conf（配置字典）读取提示词文件的相对路径
2. 转换为绝对路径避免执行目录导致的路径错误
3. 读取文件内容并返回，捕获关键异常并记录日志
"""
# ====================== 正确导入（适配 utils 同目录结构） ======================
# 说明：所有文件在 utils/ 文件夹下，直接导入同目录的兄弟文件，无需加 utils. 前缀
from utils.config_handler import prompts_conf  # 导入prompts.yml解析后的配置字典
from utils.path_tool import get_abs_path       # 导入绝对路径转换函数
from utils.logger_handler import logger        # 导入自定义日志器

# ====================== 核心函数1：加载系统主提示词 ======================
def load_system_prompts():
    """
    加载智能体核心系统提示词模板

    返回：
        str: 系统提示词文件的文本内容
    异常：
        KeyError: prompts.yml配置中缺失main_prompt_path键
        Exception: 文件读取失败（路径错误/编码问题/权限不足等）
    """
    try:
        # 步骤1：从配置中获取提示词文件相对路径，转换为绝对路径
        # get_abs_path：将配置中的相对路径转为项目根目录的绝对路径，避免路径错误
        system_prompt_path = get_abs_path(prompts_conf["main_prompt_path"])
    except KeyError as e:
        # 捕获配置项缺失异常：yaml中没有main_prompt_path配置
        logger.error(f"[load_system_prompts] 在yaml配置项中没有main_prompt_path配置项")
        raise e  # 抛出异常，让调用方感知错误（而非静默失败）

    try:
        # 步骤2：以utf-8编码读取文件内容（避免中文乱码），读取后直接返回文本
        return open(system_prompt_path, "r", encoding="utf-8").read()
    except Exception as e:
        # 捕获文件读取所有异常：文件不存在/权限不足/编码错误等
        logger.error(f"[load_system_prompts] 解析系统提示词出错，{str(e)}")
        raise e  # 抛出异常，终止流程并提示错误

# ====================== 核心函数2：加载RAG检索增强提示词 ======================
def load_rag_prompts():
    """
    加载RAG（检索增强生成）专用的总结提示词模板

    返回：
        str: RAG提示词文件的文本内容
    异常：
        KeyError: prompts.yml配置中缺失rag_summarize_prompt_path键
        Exception: 文件读取失败
    """
    try:
        # 从配置中获取RAG提示词文件路径，转换为绝对路径
        rag_prompt_path = get_abs_path(prompts_conf["rag_summarize_prompt_path"])
    except KeyError as e:
        logger.error(f"[load_rag_prompts] 在yaml配置项中没有rag_summarize_prompt_path配置项")
        raise e

    try:
        # 读取文件内容并返回
        return open(rag_prompt_path, "r", encoding="utf-8").read()
    except Exception as e:
        logger.error(f"[load_rag_prompts] 解析RAG提示词出错，{str(e)}")
        raise e

# ====================== 核心函数3：加载报告生成提示词 ======================
def load_report_prompts():
    """
    加载报告生成专用提示词模板

    返回：
        str: 报告提示词文件的文本内容
    异常：
        KeyError: prompts.yml配置中缺失report_prompt_path键
        Exception: 文件读取失败
    """
    try:
        # 从配置中获取报告提示词文件路径，转换为绝对路径
        report_prompt_path = get_abs_path(prompts_conf["report_prompt_path"])
    except KeyError as e:
        logger.error(f"[load_report_prompts] 在yaml配置项中没有report_prompt_path配置项")
        raise e

    try:
        # 读取文件内容并返回
        return open(report_prompt_path, "r", encoding="utf-8").read()
    except Exception as e:
        logger.error(f"[load_report_prompts] 解析报告生成提示词出错，{str(e)}")
        raise e

# ====================== 测试代码 ======================
if __name__ == '__main__':
    # 测试加载报告提示词并打印内容（验证函数是否正常工作）
    # 执行前需确保prompts.yml中配置了report_prompt_path，且对应文件存在
    print(load_report_prompts())