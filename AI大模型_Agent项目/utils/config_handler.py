"""
功能：加载多个 YAML 格式的配置文件（rag/chroma/prompts/agent），提供全局可调用的配置变量
核心：基于绝对路径加载配置，避免相对路径错误；使用安全的 FullLoader 解析 YAML，防止注入风险
"""
# 导入 YAML 解析库（需提前安装：pip install pyyaml）
import yaml
# 导入自定义路径工具，用于获取文件的绝对路径（确保配置文件路径不随执行目录变化）
from utils.path_tool import get_abs_path


# ====================== 通用配置加载函数（优化后，避免重复代码） ======================
def load_yaml_config(config_path: str, encoding: str = "utf-8") -> dict:
    """
    通用 YAML 配置加载函数（替代重复的单个加载函数，更易维护）

    参数：
        config_path: 配置文件的绝对路径
        encoding: 文件编码，默认 utf-8（避免中文乱码）

    返回：
        dict: 解析后的 YAML 配置字典

    异常处理：
        捕获文件不存在、YAML 语法错误、权限不足等异常，并给出明确提示
    """
    try:
        # 以只读模式打开配置文件，指定编码格式
        with open(config_path, "r", encoding=encoding) as f:
            # 使用 FullLoader 解析 YAML（安全解析，避免旧版 Loader 的安全风险）
            # yaml.load 会将 YAML 格式的键值对转换为 Python 字典
            config = yaml.load(f, Loader=yaml.FullLoader)
            # 验证解析结果是否为字典（避免空配置/非键值对配置）
            if not isinstance(config, dict):
                raise ValueError(f"配置文件 {config_path} 格式错误，需为键值对结构（k: v）")
            return config
    except FileNotFoundError:
        raise FileNotFoundError(f"配置文件不存在：{config_path}，请检查路径是否正确")
    except yaml.YAMLError as e:
        raise ValueError(f"YAML 语法错误（{config_path}）：{str(e)}")
    except PermissionError:
        raise PermissionError(f"无读取权限：{config_path}")
    except Exception as e:
        raise Exception(f"加载配置文件失败（{config_path}）：{str(e)}")


# ====================== 各模块配置加载（基于通用函数） ======================
def load_rag_config(config_path: str = get_abs_path("config/rag.yml"), encoding: str = "utf-8") -> dict:
    """加载 RAG 相关配置（如文档路径、检索参数等）"""
    return load_yaml_config(config_path, encoding)


def load_chroma_config(config_path: str = get_abs_path("config/chroma.yml"), encoding: str = "utf-8") -> dict:
    """加载 Chroma 向量数据库配置（如存储路径、嵌入模型等）"""
    return load_yaml_config(config_path, encoding)


def load_prompts_config(config_path: str = get_abs_path("config/prompts.yml"), encoding: str = "utf-8") -> dict:
    """加载提示词模板配置（如系统提示词、工具调用提示词等）"""
    return load_yaml_config(config_path, encoding)


def load_agent_config(config_path: str = get_abs_path("config/agent.yml"), encoding: str = "utf-8") -> dict:
    """加载智能体（Agent）配置（如模型名称、中间件、工具列表等）"""
    return load_yaml_config(config_path, encoding)


# ====================== 全局配置变量（加载后供其他模块导入使用） ======================
# 加载各模块配置，后续其他脚本可直接导入这些变量使用（如 from config_loader import rag_conf）
rag_conf = load_rag_config()  # RAG 配置
chroma_conf = load_chroma_config()  # Chroma 向量库配置
agent_conf = load_agent_config()  # Agent 智能体配置
prompts_conf = load_prompts_config()  # 提示词配置

# ====================== 测试代码（验证配置加载是否正常） ======================
if __name__ == '__main__':
    # 示例：读取 agent.yml 中的 chat_model_name 配置项并打印
    # 前提：agent.yml 中需包含 chat_model_name: qwen3-max 这类键值对
    print("Agent 配置中的模型名称：", agent_conf["chat_model_name"])

    # 可选：打印所有配置，验证加载完整性
    # print("RAG 配置：", rag_conf)
    # print("Chroma 配置：", chroma_conf)
    # print("提示词配置：", prompts_conf)