"""
爬虫 Agent - 专门用于网页内容爬取
"""
from src.agents.base_agent import BaseAgent
from src.tools.crawl_tools import crawl_tools
from src.constants import CRAWLER_AGENT_SYSTEM_PROMPT
from src.logger import logger
from typing import List


class CrawlerAgent(BaseAgent):
    """爬虫Agent"""
    
    def __init__(self):
        super().__init__(
            agent_type="crawler",
            name="CrawlerAgent",
            system_prompt=CRAWLER_AGENT_SYSTEM_PROMPT,
            tools=crawl_tools
        )
    
    def run(self, urls: List[str]) -> dict:
        """
        爬取网页
        
        Args:
            urls: URL列表
        
        Returns:
            爬虫结果
        """
        logger.info(f"[CrawlerAgent] 爬虫URL数: {len(urls)}")
        
        url_str = ", ".join(urls)
        user_input = f"请爬取以下URL的内容: {url_str}"
        
        result = super().run(user_input)
        
        return {
            "agent": "crawler",
            "urls": urls,
            "result": result
        }