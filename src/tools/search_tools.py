"""
搜索工具集
"""
from typing import List, Dict, Any
from pydantic import BaseModel, Field
from langchain_core.tools import tool
import json
from src.api.serpapi import serpapi_client, google_client
from src.database import db
from src.logger import logger
from src.constants import DEFAULT_SEARCH_ENGINE


class SearchInput(BaseModel):
    """搜索输入参数"""
    query: str = Field(description="搜索查询词")
    limit: int = Field(default=10, description="返回结果数量")
    engine: str = Field(default="serpapi", description="搜索引擎: serpapi 或 google")


@tool
def search_information(query: str, limit: int = 10, engine: str = DEFAULT_SEARCH_ENGINE) -> str:
    """
    搜索信息工具
    
    Args:
        query: 搜索查询
        limit: 结果数量
        engine: 搜索引擎
    
    Returns:
        JSON格式的搜索结果
    """
    try:
        logger.info(f"执行搜索: {query} (引擎: {engine})")
        
        # 先检查缓存
        cached = db.get_search_cache(query, engine)
        if cached:
            logger.info(f"使用缓存结果: {query}")
            return json.dumps(cached, ensure_ascii=False)
        
        # 执行搜索
        if engine == "google" and google_client:
            results = google_client.search(query, limit)
        else:
            results = serpapi_client.search(query, limit)
        
        # 转换为字典
        results_dict = [r.model_dump() for r in results]
        
        # 保存到缓存
        db.save_search_cache(query, results_dict, engine)
        
        return json.dumps({
            "success": True,
            "query": query,
            "engine": engine,
            "count": len(results_dict),
            "results": results_dict
        }, ensure_ascii=False)
    
    except Exception as e:
        logger.error(f"搜索失败: {str(e)}")
        return json.dumps({
            "success": False,
            "error": str(e)
        }, ensure_ascii=False)


@tool
def search_multiple_queries(queries: List[str]) -> str:
    """
    执行多个搜索查询
    
    Args:
        queries: 查询列表
    
    Returns:
        所有搜索结果
    """
    try:
        logger.info(f"执行多查询搜索: {len(queries)} 个查询")
        
        all_results = {}
        for query in queries:
            results = serpapi_client.search(query, limit=5)
            all_results[query] = [r.model_dump() for r in results]
        
        return json.dumps({
            "success": True,
            "total_queries": len(queries),
            "results": all_results
        }, ensure_ascii=False)
    
    except Exception as e:
        logger.error(f"多查询搜索失败: {str(e)}")
        return json.dumps({
            "success": False,
            "error": str(e)
        }, ensure_ascii=False)


# 导出工具列表
search_tools = [
    search_information,
    search_multiple_queries
]