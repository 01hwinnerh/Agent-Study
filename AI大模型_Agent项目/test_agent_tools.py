import json
import pytest
from unittest.mock import patch, MagicMock

# 假设我们在 agent_tools.py 导入了相关的依赖
from agent.tools.agent_tools import web_search, ddgs

def test_web_search_success():
    """测试 200 状态：正常返回搜索结果"""
    # 模拟 ddgs.text 返回正常的生成器
    mock_results = [
        {"title": "Test Title 1", "body": "Test Body 1", "href": "http://test.com/1"},
        {"title": "Test Title 2", "body": "Test Body 2", "href": "http://test.com/2"},
    ]
    with patch.object(ddgs, "text", return_value=iter(mock_results)):
        result = web_search.run("测试查询")
        assert "Test Title 1" in result
        assert "Test Title 2" in result

def test_web_search_empty():
    """测试 404 状态或空结果：返回 {"results": [], "count": 0}"""
    with patch.object(ddgs, "text", return_value=iter([])):
        result = web_search.run("不存在的内容")
        expected = json.dumps({"results": [], "count": 0})
        assert result == expected

def test_web_search_exception():
    """测试 500 状态或异常：触发 except 分支并返回 {"results": [], "count": 0}"""
    with patch.object(ddgs, "text", side_effect=Exception("API Error")):
        result = web_search.run("引发异常的查询")
        expected = json.dumps({"results": [], "count": 0})
        assert result == expected

def test_web_search_disabled():
    """测试 enable_web_search=False 状态"""
    with patch("agent.tools.agent_tools.agent_conf", {"enable_web_search": False}):
        result = web_search.run("任何查询")
        expected = json.dumps({"results": [], "count": 0})
        assert result == expected
