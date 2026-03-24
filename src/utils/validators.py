"""
数据验证和检查
"""
from typing import Any, List, Dict
import re


def is_valid_url(url: str) -> bool:
    """
    验证URL是否有效
    
    Args:
        url: URL字符串
    
    Returns:
        是否有效
    """
    url_pattern = r'^https?://[^\s/$.?#].[^\s]*$'
    return re.match(url_pattern, url) is not None


def is_valid_email(email: str) -> bool:
    """
    验证邮箱是否有效
    
    Args:
        email: 邮箱字符串
    
    Returns:
        是否有效
    """
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_pattern, email) is not None


def validate_api_key(api_key: str, min_length: int = 10) -> bool:
    """
    验证API密钥
    
    Args:
        api_key: API密钥
        min_length: 最小长度
    
    Returns:
        是否有效
    """
    if not api_key or not isinstance(api_key, str):
        return False
    return len(api_key) >= min_length


def validate_search_query(query: str) -> bool:
    """
    验证搜索查询
    
    Args:
        query: 搜索查询
    
    Returns:
        是否有效
    """
    if not query or not isinstance(query, str):
        return False
    return 1 <= len(query) <= 1000


def validate_urls(urls: List[str]) -> tuple[bool, str]:
    """
    验证URL列表
    
    Args:
        urls: URL列表
    
    Returns:
        (是否有效, 错误信息)
    """
    if not isinstance(urls, list):
        return False, "URLs 必须是列表"
    
    if len(urls) == 0:
        return False, "URLs 列表不能为空"
    
    if len(urls) > 100:
        return False, "最多只能指定100个URLs"
    
    invalid_urls = [url for url in urls if not is_valid_url(url)]
    if invalid_urls:
        return False, f"无效的URL: {', '.join(invalid_urls[:3])}"
    
    return True, ""


def validate_agent_input(agent_type: str, input_data: Dict[str, Any]) -> tuple[bool, str]:
    """
    验证Agent输入
    
    Args:
        agent_type: Agent类型
        input_data: 输入数据
    
    Returns:
        (是否有效, 错误信息)
    """
    if not agent_type:
        return False, "Agent类型不能为空"
    
    if agent_type == "search":
        query = input_data.get("query", "")
        if not validate_search_query(query):
            return False, "无效的搜索查询"
    
    elif agent_type == "crawler":
        urls = input_data.get("urls", [])
        valid, error = validate_urls(urls)
        if not valid:
            return False, error
    
    return True, ""