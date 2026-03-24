"""
Firecrawl 网页爬虫集成
"""
from firecrawl import FirecrawlApp
from typing import Optional, Dict, Any
from src.config import settings
from src.logger import logger
from src.models.schemas import CrawledContent
import asyncio


class FirecrawlClient:
    """Firecrawl 客户端"""
    
    def __init__(self):
        self.api_key = settings.firecrawl_api_key
        if not self.api_key:
            raise ValueError("FIRECRAWL_API_KEY 未设置")
        
        self.app = FirecrawlApp(api_key=self.api_key)
    
    def crawl_url(
        self,
        url: str,
        include_markdown: bool = True,
        include_html: bool = False,
        timeout: Optional[int] = None
    ) -> CrawledContent:
        """
        爬取单个URL
        
        Args:
            url: 要爬取的URL
            include_markdown: 是否返回Markdown格式
            include_html: 是否返回HTML
            timeout: 超时时间（秒）
        
        Returns:
            爬取的内容
        """
        try:
            logger.info(f"开始爬取URL: {url}")
            
            result = self.app.scrape_url(url)
            
            if result.get("success"):
                content = CrawledContent(
                    url=url,
                    title=result.get("metadata", {}).get("title", ""),
                    content=result.get("content", ""),
                    markdown=result.get("markdown", "") if include_markdown else None,
                    metadata=result.get("metadata", {}),
                    success=True
                )
                logger.info(f"URL爬取成功: {url}")
                return content
            else:
                error_msg = result.get("error", "未知错误")
                logger.warning(f"URL爬取失败: {url} - {error_msg}")
                return CrawledContent(
                    url=url,
                    title="",
                    content="",
                    success=False,
                    error_message=error_msg
                )
        
        except Exception as e:
            logger.error(f"爬取异常: {url} - {str(e)}")
            return CrawledContent(
                url=url,
                title="",
                content="",
                success=False,
                error_message=str(e)
            )
    
    def crawl_urls(
        self,
        urls: list,
        include_markdown: bool = True
    ) -> list:
        """
        批量爬取URLs
        
        Args:
            urls: URL列表
            include_markdown: 是否返回Markdown格式
        
        Returns:
            爬取结果列表
        """
        results = []
        for url in urls:
            content = self.crawl_url(url, include_markdown=include_markdown)
            results.append(content)
        
        return results


# 全局Firecrawl客户端
try:
    firecrawl_client = FirecrawlClient()
except Exception as e:
    logger.error(f"Firecrawl 初始化失败: {str(e)}")
    firecrawl_client = None