"""
报告生成 Agent - 专门用于生成分析报告
"""
from src.agents.base_agent import BaseAgent
from src.tools.report_tools import report_tools
from src.constants import REPORTER_AGENT_SYSTEM_PROMPT
from src.logger import logger
from typing import List


class ReporterAgent(BaseAgent):
    """报告生成Agent"""
    
    def __init__(self):
        super().__init__(
            agent_type="reporter",
            name="ReporterAgent",
            system_prompt=REPORTER_AGENT_SYSTEM_PROMPT,
            tools=report_tools
        )
    
    def run(
        self,
        title: str,
        content: str,
        data_sources: List[str],
        report_type: str = "analysis"
    ) -> dict:
        """
        生成报告
        
        Args:
            title: 报告标题
            content: 报告内容
            data_sources: 数据来源
            report_type: 报告类型
        
        Returns:
            报告生成结果
        """
        logger.info(f"[ReporterAgent] 生成报告: {title}")
        
        user_input = f"""
        请生成一份 {report_type} 类型的报告，标题为: {title}
        
        主要内容:
        {content[:500]}
        
        数据来源:
        {', '.join(data_sources)}
        """
        
        result = super().run(user_input)
        
        return {
            "agent": "reporter",
            "title": title,
            "report_type": report_type,
            "sources_count": len(data_sources),
            "result": result
        }