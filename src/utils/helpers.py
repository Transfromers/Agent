"""
工具函数和辅助方法
"""
import json
import hashlib
from typing import Any, Dict, List
from datetime import datetime


def safe_json_dumps(data: Any, max_length: int = 1000) -> str:
    """
    安全的JSON序列化
    
    Args:
        data: 数据对象
        max_length: 最大长度
    
    Returns:
        JSON字符串
    """
    try:
        json_str = json.dumps(data, ensure_ascii=False, indent=2)
        if len(json_str) > max_length:
            return json_str[:max_length] + "..."
        return json_str
    except Exception as e:
        return f"序列化失败: {str(e)}"


def truncate_text(text: str, max_length: int = 500) -> str:
    """
    截断文本
    
    Args:
        text: 文本
        max_length: 最大长度
    
    Returns:
        截断后的文本
    """
    if len(text) > max_length:
        return text[:max_length] + "..."
    return text


def generate_id(prefix: str = "") -> str:
    """
    生成唯一ID
    
    Args:
        prefix: ID前缀
    
    Returns:
        唯一ID
    """
    timestamp = datetime.now().isoformat()
    hash_obj = hashlib.md5(timestamp.encode())
    return f"{prefix}_{hash_obj.hexdigest()[:8]}"


def merge_dicts(*dicts: Dict[str, Any]) -> Dict[str, Any]:
    """
    合并多个字典
    
    Args:
        *dicts: 字典列表
    
    Returns:
        合并后的字典
    """
    result = {}
    for d in dicts:
        result.update(d)
    return result


def format_duration(seconds: float) -> str:
    """
    格式化时间持续
    
    Args:
        seconds: 秒数
    
    Returns:
        格式化的时间字符串
    """
    if seconds < 60:
        return f"{seconds:.2f}s"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.2f}m"
    else:
        hours = seconds / 3600
        return f"{hours:.2f}h"


def extract_urls(text: str) -> List[str]:
    """
    从文本中提取URL
    
    Args:
        text: 文本
    
    Returns:
        URL列表
    """
    import re
    url_pattern = r'https?://[^\s\])]+'
    return re.findall(url_pattern, text)


def extract_emails(text: str) -> List[str]:
    """
    从文本中提取邮箱
    
    Args:
        text: 文本
    
    Returns:
        邮箱列表
    """
    import re
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.findall(email_pattern, text)