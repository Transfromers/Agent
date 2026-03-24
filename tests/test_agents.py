"""
Agent 单元测试
"""
import pytest
from src.agents.search_agent import SearchAgent
from src.agents.crawler_agent import CrawlerAgent
from src.agents.analyzer_agent import AnalyzerAgent
from src.agents.reporter_agent import ReporterAgent
from src.agents.orchestrator import AgentOrchestrator


class TestSearchAgent:
    """搜索Agent测试"""
    
    def test_initialization(self):
        """测试初始化"""
        agent = SearchAgent()
        assert agent is not None
        assert agent.name == "SearchAgent"
        assert agent.agent_type == "search"
    
    def test_search_execution(self):
        """测试搜索执行"""
        agent = SearchAgent()
        result = agent.run("Python 编程")
        assert result is not None
        assert "agent" in result
        assert result["agent"] == "search"


class TestCrawlerAgent:
    """爬虫Agent测试"""
    
    def test_initialization(self):
        """测试初始化"""
        agent = CrawlerAgent()
        assert agent is not None
        assert agent.name == "CrawlerAgent"
        assert agent.agent_type == "crawler"


class TestAnalyzerAgent:
    """分析Agent测试"""
    
    def test_initialization(self):
        """测试初始化"""
        agent = AnalyzerAgent()
        assert agent is not None
        assert agent.name == "AnalyzerAgent"
        assert agent.agent_type == "analyzer"


class TestReporterAgent:
    """报告Agent测试"""
    
    def test_initialization(self):
        """测试初始化"""
        agent = ReporterAgent()
        assert agent is not None
        assert agent.name == "ReporterAgent"
        assert agent.agent_type == "reporter"


class TestOrchestrator:
    """编排器测试"""
    
    def test_initialization(self):
        """测试初始化"""
        orchestrator = AgentOrchestrator()
        assert orchestrator is not None
        assert orchestrator.search_agent is not None
        assert orchestrator.crawler_agent is not None
        assert orchestrator.analyzer_agent is not None
        assert orchestrator.reporter_agent is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])