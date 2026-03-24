
"""
DuckDuckGo 搜索引擎集成
"""
from duckduckgo_search import DDGS
from typing import List
from src.models.schemas import SearchResult
from src.logger import logger

class DuckDuckGoSearchClient:
    """DuckDuckGo 客户端"""

    def __init__(self):
        self.client = DDGS()

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        """
        执行搜索查询
        
        Args:
            query: 搜索查询
            limit: 返回结果数量
        
        Returns:
            搜索结果列表
        """
        try:
            logger.info(f"DuckDuckGo 搜索: {query}")
            
            results = self.client.text(query, max_results=limit)
            
            parsed_results = self._parse_results(results)
            
            logger.info(f"搜索完成，获得 {len(parsed_results)} 条结果")
            return parsed_results
            
        except Exception as e:
            logger.error(f"DuckDuckGo 搜索失败: {str(e)}")
            return []

    def _parse_results(self, results: list) -> List[SearchResult]:
        """解析搜索结果"""
        parsed = []
        for i, item in enumerate(results):
            result = SearchResult(
                title=item.get("title", ""),
                url=item.get("href", ""),
                snippet=item.get("body", ""),
                source="duckduckgo",
                relevance_score=1.0 - (i * 0.05)
            )
            parsed.append(result)
        return parsed

# 全局客户端实例
duckduckgo_client = DuckDuckGoSearchClient()
