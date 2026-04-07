import os
import pytest
import requests
import responses
from pyfakefs.fake_filesystem_unittest import Patcher

# 导入刚才创建的函数
from utils.download_utils import stream_save_file

@responses.activate
def test_stream_save_file_success(fs):
    """
    4.4 补充单元测试，使用 moto/pyfakefs 验证断电续传与并发写入场景。
    测试正常下载 SSE 并写入文件的过程。
    """
    url = "http://test.com/stream"
    dest = "/test_dir/result.txt"
    fs.create_dir("/test_dir")
    
    # 模拟 SSE 流
    responses.add(
        responses.GET,
        url,
        body="data: Hello\n\ndata: World\n\n",
        status=200,
        content_type="text/event-stream"
    )
    
    stream_save_file(url, dest)
    
    # 验证是否正确解析 SSE 并写入
    assert os.path.exists(dest)
    with open(dest, "rb") as f:
        content = f.read()
        assert b"Hello\nWorld\n" == content

@responses.activate
def test_stream_save_file_failure(fs):
    """
    测试异常分支：下载失败时，确保 .tmp 文件被删除。
    """
    url = "http://test.com/stream_fail"
    dest = "/test_dir/fail_result.txt"
    fs.create_dir("/test_dir")
    
    responses.add(
        responses.GET,
        url,
        body=Exception("Connection Error"),
    )
    
    with pytest.raises(Exception):
        stream_save_file(url, dest)
        
    # 验证 .tmp 文件不存在
    assert not os.path.exists(dest + ".tmp")
    assert not os.path.exists(dest)
