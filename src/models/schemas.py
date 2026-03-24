"""
数据模型和序列化模式
"""
from pydantic import BaseModel, Field
from typing import Any, Optional, List
from datetime import datetime
from enum import Enum


class SearchResult(BaseModel):
    """搜索结果模型"""
    title: str
    url: str
    snippet: str
    source: str = "unknown"
    relevance_score: float = 0.0
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Example Title",
                "url": "https://example.com",
                "snippet": "Example snippet...",
                "source": "google",
                "relevance_score": 0.95
            }
        }


class CrawledContent(BaseModel):
    """爬取的网页内容"""
    url: str
    title: str
    content: str
    markdown: Optional[str] = None
    metadata: dict = Field(default_factory=dict)
    crawl_time: datetime = Field(default_factory=datetime.now)
    success: bool = True
    error_message: Optional[str] = None


class AnalysisResult(BaseModel):
    """分析结果"""
    key_points: List[str]
    summary: str
    insights: List[str]
    data_quality_score: float
    analysis_timestamp: datetime = Field(default_factory=datetime.now)


class Report(BaseModel):
    """生成的报告"""
    title: str
    executive_summary: str
    main_content: str
    key_findings: List[str]
    recommendations: List[str]
    data_sources: List[str]
    generation_time: datetime = Field(default_factory=datetime.now)
    report_type: str = "analysis"


class TaskResult(BaseModel):
    """任务执行结果"""
    task_id: str
    agent_type: str
    status: str
    input_data: dict
    output_data: Optional[dict] = None
    error: Optional[str] = None
    execution_time: float = 0.0
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class AgentState(BaseModel):
    """Agent 状态"""
    messages: List[dict]
    task_data: dict = Field(default_factory=dict)
    search_results: List[SearchResult] = Field(default_factory=list)
    crawled_content: List[CrawledContent] = Field(default_factory=list)
    analysis_results: Optional[AnalysisResult] = None
    final_report: Optional[Report] = None
    error_log: List[str] = Field(default_factory=list)