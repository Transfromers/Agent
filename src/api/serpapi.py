"""
SerpAPI 搜索引擎集成
"""
import requests
from typing import List, Dict, Any
from src.config import settings
from src.logger import logger
from src.models.schemas import SearchResult
import json


class SerpAPIClient:
    """SerpAPI 客户端"""
    
    BASE_URL = "https://serpapi.com/search"
    
    def __init__(self):
        self.api_key = settings.serpapi_api_key
        if not self.api_key:
            raise ValueError("SERPAPI_API_KEY 未设置")
    
    def search(
        self,
        query: str,
        limit: int = 10,
        language: str = "en",
        region: str = "us"
    ) -> List[SearchResult]:
        """
        执行搜索查询
        
        Args:
            query: 搜索查询
            limit: 返回结果数量
            language: 搜索语言
            region: 搜索地区
        
        Returns:
            搜索结果列表
        """
        try:
            logger.info(f"SerpAPI 搜索: {query}")
            
            params = {
                "q": query,
                "api_key": self.api_key,
                "num": limit,
                "hl": language,
                "gl": region,
            }
            
            response = requests.get(
                self.BASE_URL,
                params=params,
                timeout=settings.timeout
            )
            response.raise_for_status()
            
            data = response.json()
            results = self._parse_results(data)
            
            logger.info(f"搜索完成，获得 {len(results)} 条结果")
            return results
            
        except requests.exceptions.RequestException as e:
            error_message = f"SerpAPI 请求失败: {e.__class__.__name__}, URL: {e.request.url if e.request else 'N/A'}, Error: {str(e)}"
            if e.response is not None:
                error_message += f", Status Code: {e.response.status_code}, Response: {e.response.text}"
            logger.error(error_message)
            return []
        except Exception as e:
            logger.error(f"搜索处理失败: {str(e)}")
            return []
    
    def _parse_results(self, data: Dict[str, Any]) -> List[SearchResult]:
        """解析搜索结果"""
        results = []
        
        # 有���搜索结果
        organic_results = data.get("organic_results", [])
        for i, item in enumerate(organic_results):
            result = SearchResult(
                title=item.get("title", ""),
                url=item.get("link", ""),
                snippet=item.get("snippet", ""),
                source="serpapi",
                relevance_score=1.0 - (i * 0.05)  # 排名越靠前分数越高
            )
            results.append(result)
        
        return results


class GoogleSearchClient:
    """Google Custom Search API 客户端"""
    
    BASE_URL = "https://www.googleapis.com/customsearch/v1"
    
    def __init__(self):
        self.api_key = settings.google_api_key
        self.search_engine_id = settings.google_search_engine_id
        
        if not self.api_key or not self.search_engine_id:
            logger.warning("Google Search API 凭证未设置")
    
    def search(
        self,
        query: str,
        limit: int = 10
    ) -> List[SearchResult]:
        """执行搜索查询"""
        
        if not self.api_key or not self.search_engine_id:
            logger.error("Google Search API 凭证未配置")
            return []
        
        try:
            logger.info(f"Google Search 搜索: {query}")
            
            params = {
                "key": self.api_key,
                "cx": self.search_engine_id,
                "q": query,
                "num": min(limit, 10)
            }
            
            response = requests.get(
                self.BASE_URL,
                params=params,
                timeout=settings.timeout
            )
            response.raise_for_status()
            
            data = response.json()
            results = self._parse_results(data)
            
            logger.info(f"搜索完成，获得 {len(results)} 条结果")
            return results
            
        except Exception as e:
            logger.error(f"Google Search 搜索失败: {str(e)}")
            return []
    
    def _parse_results(self, data: Dict[str, Any]) -> List[SearchResult]:
        """解析搜索结果"""
        results = []
        
        items = data.get("items", [])
        for i, item in enumerate(items):
            result = SearchResult(
                title=item.get("title", ""),
                url=item.get("link", ""),
                snippet=item.get("snippet", ""),
                source="google",
                relevance_score=1.0 - (i * 0.05)
            )
            results.append(result)
        
        return results


# 全局客户端实例
serpapi_client = SerpAPIClient()
try:
    google_client = GoogleSearchClient()
except:
    google_client = None