"""
数据处理和分析工具集
"""
from pydantic import BaseModel, Field
from langchain_core.tools import tool
import json
from typing import List
from src.logger import logger


class DataProcessInput(BaseModel):
    """数据处理输入"""
    data: str = Field(description="要处理的数据")
    action: str = Field(description="处理操作: summarize/extract/analyze/clean")


@tool
def process_text_data(data: str, action: str = "summarize") -> str:
    """
    处理和分析文本数据
    
    Args:
        data: 输入数据
        action: 操作类型
    
    Returns:
        处理结果
    """
    try:
        logger.info(f"处理数据: {action}")
        
        if action == "summarize":
            # 简单的摘要（提取前500个字符）
            summary = data[:500] if len(data) > 500 else data
            return json.dumps({
                "success": True,
                "action": "summarize",
                "result": summary,
                "original_length": len(data),
                "summary_length": len(summary)
            }, ensure_ascii=False)
        
        elif action == "extract":
            # 提取关键词
            words = data.split()[:20]
            return json.dumps({
                "success": True,
                "action": "extract",
                "keywords": words,
                "count": len(words)
            }, ensure_ascii=False)
        
        elif action == "analyze":
            # 基础分析
            word_count = len(data.split())
            char_count = len(data)
            avg_word_length = char_count / word_count if word_count > 0 else 0
            
            return json.dumps({
                "success": True,
                "action": "analyze",
                "statistics": {
                    "word_count": word_count,
                    "char_count": char_count,
                    "avg_word_length": round(avg_word_length, 2),
                    "sentence_count": data.count(".")
                }
            }, ensure_ascii=False)
        
        elif action == "clean":
            # 清理数据
            cleaned = data.strip()
            cleaned = " ".join(cleaned.split())  # 移除多余空格
            
            return json.dumps({
                "success": True,
                "action": "clean",
                "original_length": len(data),
                "cleaned_length": len(cleaned),
                "data": cleaned
            }, ensure_ascii=False)
        
        else:
            return json.dumps({
                "success": False,
                "error": f"未知操作: {action}"
            }, ensure_ascii=False)
    
    except Exception as e:
        logger.error(f"数据处理失败: {str(e)}")
        return json.dumps({
            "success": False,
            "error": str(e)
        }, ensure_ascii=False)


@tool
def extract_key_information(data: str, keywords: List[str]) -> str:
    """
    根据关键词提取信息
    
    Args:
        data: 输入数据
        keywords: 关键词列表
    
    Returns:
        包含关键词的句子
    """
    try:
        logger.info(f"提取关键信息，关键词数: {len(keywords)}")
        
        sentences = data.split(".")
        relevant_sentences = []
        
        for sentence in sentences:
            for keyword in keywords:
                if keyword.lower() in sentence.lower():
                    relevant_sentences.append(sentence.strip())
                    break
        
        return json.dumps({
            "success": True,
            "keywords": keywords,
            "relevant_count": len(relevant_sentences),
            "relevant_sentences": relevant_sentences[:10]  # 限制返回数量
        }, ensure_ascii=False)
    
    except Exception as e:
        logger.error(f"信息提取失败: {str(e)}")
        return json.dumps({
            "success": False,
            "error": str(e)
        }, ensure_ascii=False)


# 导出工具列表
data_tools = [
    process_text_data,
    extract_key_information
]