import os
import tempfile
import requests

def stream_save_file(url: str, dest_path: str):
    """
    4.1 将 response.iter_content() 改为 iter_lines() 并按 SSE 规范解析；
    4.2 在异常分支确保临时文件句柄关闭并删除 .tmp 文件；
    4.3 写入完成后做 fsync 再 rename，防止落盘不完整；
    """
    tmp_path = dest_path + ".tmp"
    
    try:
        with requests.get(url, stream=True) as response:
            response.raise_for_status()
            
            # 4.1 改为 iter_lines 并解析 SSE
            with open(tmp_path, "wb") as f:
                for line in response.iter_lines():
                    if line:
                        # 模拟 SSE 解析，去掉 data: 前缀
                        decoded_line = line.decode('utf-8')
                        if decoded_line.startswith("data: "):
                            data = decoded_line[6:].encode('utf-8') + b'\n'
                            f.write(data)
                
                # 4.3 写入完成后做 fsync 再 rename，防止落盘不完整
                f.flush()
                os.fsync(f.fileno())
                
        os.rename(tmp_path, dest_path)
    except Exception as e:
        # 4.2 在异常分支确保临时文件句柄关闭并删除 .tmp 文件
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        raise e
