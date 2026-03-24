"""
分析 Agent - 专门用于数据分析
"""
from src.agents.base_agent import BaseAgent
from src.tools.data_tools import data_tools
from src.constants import ANALYZER_AGENT_SYSTEM_PROMPT
from src.logger import logger


class AnalyzerAgent(BaseAgent):
    """分析Agent"""
    
    def __init__(self):
        super().__init__(
            agent_type="analyzer",
            name="AnalyzerAgent",
            system_prompt=ANALYZER_AGENT_SYSTEM_PROMPT,
            tools=data_tools
        )
    
    def run(self, data: str, analysis_type: str = "summarize") -> dict:
        """
        分析数据
        
        Args:
            data: 输入数据
            analysis_type: 分析类型
        
        Returns:
            分析结果
        """
        logger.info(f"[AnalyzerAgent] 分析数据，类型: {analysis_type}")
        
        user_input = f"请对以下数据进行 {analysis_type} 分析: {data[:500]}"
        
        result = super().run(user_input)
        
        return {
            "agent": "analyzer",
            "analysis_type": analysis_type,
            "data_length": len(data),
            "result": result
        }