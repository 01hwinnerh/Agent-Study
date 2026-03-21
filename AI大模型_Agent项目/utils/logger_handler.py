# 导入Python内置的日志模块，用于实现日志记录功能
import logging
# 导入自定义的路径工具函数，用于获取文件的绝对路径（需确保path_tool.py存在）
from utils.path_tool import get_abs_path

# 导入操作系统相关模块，用于目录/文件路径处理、创建目录等
import os
# 导入时间相关模块：time用于时间类型，datetime用于日期时间格式化
from datetime import time, datetime

# ====================== 全局配置常量 ======================
# 日志文件保存的根目录：通过get_abs_path获取"logs"文件夹的绝对路径
# 好处：无论脚本在哪个目录执行，都能准确定位日志目录，避免相对路径错误
LOG_ROOT = get_abs_path("logs")

# 确保日志根目录存在：exist_ok=True表示如果目录已存在，不会抛出异常
# 避免因目录不存在导致日志文件无法写入的问题
os.makedirs(LOG_ROOT, exist_ok=True)

# 日志格式配置：定义日志输出的内容和格式
# 格式说明：
# %(asctime)s: 日志记录的时间（如2026-03-21 17:30:00）
# %(name)s: 日志器的名称（如"agent"）
# %(levelname)s: 日志级别（DEBUG/INFO/WARNING/ERROR/CRITICAL）
# %(filename)s: 产生日志的文件名（如log_config.py）
# %(lineno)d: 产生日志的代码行号（便于定位问题）
# %(message)s: 日志的具体内容
DEFAULT_LOG_FORMAT = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
)


# ====================== 核心日志器创建函数 ======================
def get_logger(
        name: str = "agent",  # 日志器名称，默认"agent"，用于区分不同模块的日志
        console_level: int = logging.INFO,  # 控制台输出的日志级别，默认INFO（只输出INFO及以上）
        file_level: int = logging.DEBUG,  # 文件保存的日志级别，默认DEBUG（保存所有级别日志）
        log_file=None,  # 自定义日志文件名，默认None（自动生成）
) -> logging.Logger:
    """
    创建并配置一个可同时输出到控制台和文件的日志器

    参数说明：
    - name: 日志器名称，不同名称对应不同的日志器实例，避免日志混淆
    - console_level: 控制台日志级别（DEBUG<INFO<WARNING<ERROR<CRITICAL）
    - file_level: 日志文件级别，通常设置为DEBUG以保存更详细的调试信息
    - log_file: 自定义日志文件路径，不传则自动生成「名称_日期.log」格式的文件

    返回值：
    - logging.Logger: 配置完成的日志器实例
    """
    # 获取/创建指定名称的日志器实例
    # 注意：logging.getLogger是单例模式，同名日志器只会创建一次
    logger = logging.getLogger(name)

    # 设置日志器的基础级别为DEBUG（必须低于console/file级别，否则会被过滤）
    # 例如：如果这里设为INFO，即使file_level设为DEBUG，文件也不会保存DEBUG日志
    logger.setLevel(logging.DEBUG)

    # 关键：避免重复添加处理器（Handler），防止日志重复打印
    # 场景：多次调用get_logger时，若不判断，会重复添加Console/File Handler，导致一条日志打印多次
    if logger.handlers:
        return logger

    # ====================== 1. 配置控制台日志处理器 ======================
    # 创建控制台处理器：将日志输出到终端/控制台
    console_handler = logging.StreamHandler()
    # 设置控制台日志级别：只输出该级别及以上的日志（默认INFO，过滤DEBUG）
    console_handler.setLevel(console_level)
    # 绑定日志格式：使用全局定义的DEFAULT_LOG_FORMAT
    console_handler.setFormatter(DEFAULT_LOG_FORMAT)
    # 将控制台处理器添加到日志器
    logger.addHandler(console_handler)

    # ====================== 2. 配置文件日志处理器 ======================
    # 如果未传入自定义日志文件名，则自动生成
    if not log_file:
        # 生成格式：日志根目录/名称_年月日.log（如logs/agent_20260321.log）
        log_file = os.path.join(LOG_ROOT, f"{name}_{datetime.now().strftime('%Y%m%d')}.log")

    # 创建文件处理器：将日志写入指定文件，编码设为utf-8避免中文乱码
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    # 设置文件日志级别：默认DEBUG，保存所有级别的日志（便于事后调试）
    file_handler.setLevel(file_level)
    # 绑定日志格式
    file_handler.setFormatter(DEFAULT_LOG_FORMAT)
    # 将文件处理器添加到日志器
    logger.addHandler(file_handler)

    # 返回配置完成的日志器
    return logger


# ====================== 快捷使用：创建默认日志器实例 ======================
# 直接调用get_logger()创建默认配置的日志器，其他模块可直接导入这个logger使用
# 例如：from log_config import logger
logger = get_logger()

# ====================== 测试代码：验证日志功能 ======================
if __name__ == '__main__':
    # 测试不同级别的日志输出
    logger.info("信息日志")  # 控制台+文件都会输出
    logger.error("错误日志")  # 控制台+文件都会输出
    logger.warning("警告日志")  # 控制台+文件都会输出
    logger.debug("调试日志")  # 仅文件输出（控制台级别为INFO，过滤DEBUG）