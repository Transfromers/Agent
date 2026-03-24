"""
网页爬虫工具集
"""
from typing import List
from pydantic import BaseModel, Field
from langchain_core.tools import tool
import json
from src.api.firecrawl import firecrawl_client
from src.logger import logger


class CrawlInput(BaseModel):
    """爬虫输入参数"""
    url: str = Field(description="要爬取的URL")
    include_markdown: bool = Field(default=True, description="是否返回Markdown格式")


@tool
def crawl_webpage(url: str, include_markdown: bool = True) -> str:
    """
    爬取单个网页
    
    Args:
        url: 网页URL
        include_markdown: 是否返回Markdown
    
    Returns:
        爬取的内容
    """
    if not firecrawl_client:
        return json.dumps({
            "success": False,
            "error": "Firecrawl 客户端未初始化"
        }, ensure_ascii=False)
    
    try:
        logger.info(f"爬取网页: {url}")
        
        content = firecrawl_client.crawl_url(url, include_markdown=include_markdown)
        
        return json.dumps({
            "success": content.success,
            "url": content.url,
            "title": content.title,
            "content": content.content[:1000] if content.content else "",  # 限制长度
            "markdown": content.markdown[:1000] if content.markdown else "",
            "error": content.error_message
        }, ensure_ascii=False)
    
    except Exception as e:
        logger.error(f"爬取失败: {str(e)}")
        return json.dumps({
            "success": False,
            "error": str(e)
        }, ensure_ascii=False)


@tool
def crawl_multiple_urls(urls: List[str]) -> str:
    """
    批量爬取多个URL
    
    Args:
        urls: URL列表
    
    Returns:
        所有爬取结果
    """
    if not firecrawl_client:
        return json.dumps({
            "success": False,
            "error": "Firecrawl 客户端未初始化"
        }, ensure_ascii=False)
    
    try:
        logger.info(f"批量爬取 {len(urls)} 个URL")
        
        results = firecrawl_client.crawl_urls(urls)
        
        results_dict = []
        for content in results:
            results_dict.append({
                "url": content.url,
                "title": content.title,
                "success": content.success,
                "error": content.error_message
            })
        
        return json.dumps({
            "success": True,
            "total_urls": len(urls),
            "successful": sum(1 for r in results if r.success),
            "results": results_dict
        }, ensure_ascii=False)
    
    except Exception as e:
        logger.error(f"批量爬取失败: {str(e)}")
        return json.dumps({
            "success": False,
            "error": str(e)
        }, ensure_ascii=False)


# 导出工具列表
crawl_tools = [
    crawl_webpage,
    crawl_multiple_urls
]