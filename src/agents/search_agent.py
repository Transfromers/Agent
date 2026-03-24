"""
搜索 Agent - 专门用于信息搜索
"""
from src.agents.base_agent import BaseAgent
from src.tools.search_tools import search_tools
from src.constants import SEARCH_AGENT_SYSTEM_PROMPT
from src.logger import logger


class SearchAgent(BaseAgent):
    """搜索Agent"""
    
    def __init__(self):
        super().__init__(
            agent_type="search",
            name="SearchAgent",
            system_prompt=SEARCH_AGENT_SYSTEM_PROMPT,
            tools=search_tools
        )
    
    def run(self, query: str, search_engine: str = "serpapi") -> dict:
        """
        执行搜索
        
        Args:
            query: 搜索查询
            search_engine: 搜索引擎
        
        Returns:
            搜索结果
        """
        logger.info(f"[SearchAgent] 搜索查询: {query}")
        
        user_input = f"请搜索以下内容，使用 {search_engine} 搜索引擎: {query}"
        
        result = super().run(user_input)
        
        return {
            "agent": "search",
            "query": query,
            "engine": search_engine,
            "result": result
        }