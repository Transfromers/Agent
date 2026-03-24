"""
报告生成工具集
"""
from pydantic import BaseModel, Field
from langchain_core.tools import tool
import json
from datetime import datetime
from typing import List, Dict, Any
from src.logger import logger


class ReportInput(BaseModel):
    """报告生成输入"""
    title: str = Field(description="报告标题")
    content: str = Field(description="报告内容")
    data_sources: List[str] = Field(description="数据来源列表")
    report_type: str = Field(default="analysis", description="报告类型")


@tool
def generate_report(
    title: str,
    content: str,
    data_sources: List[str],
    report_type: str = "analysis"
) -> str:
    """
    生成专业报告
    
    Args:
        title: 报告标题
        content: 报告主要内容
        data_sources: 数据来源
        report_type: 报告类型
    
    Returns:
        生成的报告
    """
    try:
        logger.info(f"生成报告: {title}")
        
        # 生成报告头
        header = f"""
{'='*60}
{title}
{'='*60}
报告类型: {report_type}
生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*60}
"""
        
        # 数据来源部分
        sources_section = "\n### 数据来源\n"
        for source in data_sources:
            sources_section += f"- {source}\n"
        
        # 组合报告
        report = header + "\n" + content + "\n" + sources_section
        
        return json.dumps({
            "success": True,
            "report": report,
            "title": title,
            "type": report_type,
            "sources_count": len(data_sources)
        }, ensure_ascii=False)
    
    except Exception as e:
        logger.error(f"报告生成失败: {str(e)}")
        return json.dumps({
            "success": False,
            "error": str(e)
        }, ensure_ascii=False)


@tool
def format_findings(findings: List[str], recommendations: List[str]) -> str:
    """
    格式化发现和建议
    
    Args:
        findings: 发现列表
        recommendations: 建议列表
    
    Returns:
        格式化的文本
    """
    try:
        logger.info(f"格式化发现和建议")
        
        findings_text = "## 主要发现\n"
        for i, finding in enumerate(findings, 1):
            findings_text += f"{i}. {finding}\n"
        
        recommendations_text = "\n## 建议\n"
        for i, rec in enumerate(recommendations, 1):
            recommendations_text += f"{i}. {rec}\n"
        
        formatted = findings_text + recommendations_text
        
        return json.dumps({
            "success": True,
            "formatted_text": formatted,
            "findings_count": len(findings),
            "recommendations_count": len(recommendations)
        }, ensure_ascii=False)
    
    except Exception as e:
        logger.error(f"格式化失败: {str(e)}")
        return json.dumps({
            "success": False,
            "error": str(e)
        }, ensure_ascii=False)


# 导出工具列表
report_tools = [
    generate_report,
    format_findings
]