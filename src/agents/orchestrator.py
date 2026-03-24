"""
Agent 编排器 - 协调多个Agent的执行
"""
from typing import List, Dict, Any, Optional
from src.agents.search_agent import SearchAgent
from src.agents.crawler_agent import CrawlerAgent
from src.agents.analyzer_agent import AnalyzerAgent
from src.agents.reporter_agent import ReporterAgent
from src.logger import logger
from src.database import db, TaskRecord
import time
import uuid


class AgentOrchestrator:
    """Agent 编排器 - 管理多个Agent的协调执行"""
    
    def __init__(self):
        """初始化编排器"""
        self.search_agent = SearchAgent()
        self.crawler_agent = CrawlerAgent()
        self.analyzer_agent = AnalyzerAgent()
        self.reporter_agent = ReporterAgent()
        
        self.execution_history = []
        logger.info("AgentOrchestrator 初始化完成")
    
    def research_and_report(
        self,
        topic: str,
        search_queries: List[str],
        crawl_urls: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        完整的研究和报告生成流程
        
        Args:
            topic: 研究主题
            search_queries: 搜索查询列表
            crawl_urls: 要爬取的URL列表
        
        Returns:
            完整的研究报告
        """
        task_id = str(uuid.uuid4())
        start_time = time.time()
        
        logger.info(f"[Orchestrator] 开始研究任务: {task_id}")
        
        try:
            # 步骤1: 搜索相关信息
            logger.info(f"[Orchestrator] 步骤1: 搜索信息")
            search_results = {}
            for query in search_queries:
                result = self.search_agent.run(query)
                search_results[query] = result
                time.sleep(1)  # 避免API速率限制
            
            # 如果搜索失败，则尝试使用备用URL进行爬取
            if not any(search_results.values()) and not crawl_urls:
                logger.warning("[Orchestrator] 搜索失败，尝试使用备用URL进行爬取")
                crawl_urls = ["https://www.google.com/search?q=" + topic, "https://www.bing.com/search?q=" + topic]

            # 步骤2: 如果提供了URL，则爬取内容
            crawl_results = {}
            if crawl_urls:
                logger.info(f"[Orchestrator] 步骤2: 爬取网页")
                result = self.crawler_agent.run(crawl_urls)
                crawl_results = result
                time.sleep(1)
            
            # 步骤3: 分析收集的数据
            logger.info(f"[Orchestrator] 步骤3: 分析数据")
            combined_content = self._combine_results(search_results, crawl_results)
            analysis_result = self.analyzer_agent.run(
                combined_content,
                analysis_type="analyze"
            )
            
            # 步骤4: 生成最终报告
            logger.info(f"[Orchestrator] 步骤4: 生成报告")
            sources = search_queries + (crawl_urls or [])
            report_result = self.reporter_agent.run(
                title=f"关于 '{topic}' 的研究报告",
                content=analysis_result.get("result", ""),
                data_sources=sources,
                report_type="research"
            )
            
            execution_time = time.time() - start_time
            
            # 保存任务记录
            task_record = TaskRecord(
                id=task_id,
                agent_type="orchestrator",
                status="completed",
                input_data={
                    "topic": topic,
                    "search_queries": search_queries,
                    "crawl_urls": crawl_urls or []
                },
                output_data={
                    "search_results_count": len(search_results),
                    "crawl_results_count": len(crawl_results),
                    "analysis": analysis_result,
                    "report": report_result
                },
                execution_time=execution_time
            )
            db.save_task(task_record)
            
            logger.info(f"[Orchestrator] 任务完成: {task_id}, 耗时: {execution_time:.2f}s")
            
            return {
                "task_id": task_id,
                "status": "success",
                "topic": topic,
                "execution_time": execution_time,
                "search_results": search_results,
                "crawl_results": crawl_results,
                "analysis": analysis_result,
                "report": report_result
            }
        
        except Exception as e:
            logger.error(f"[Orchestrator] 任务失败: {task_id} - {str(e)}")
            
            # 保存错误记录
            task_record = TaskRecord(
                id=task_id,
                agent_type="orchestrator",
                status="failed",
                input_data={
                    "topic": topic,
                    "search_queries": search_queries,
                    "crawl_urls": crawl_urls or []
                },
                error_message=str(e),
                execution_time=time.time() - start_time
            )
            db.save_task(task_record)
            
            return {
                "task_id": task_id,
                "status": "failed",
                "error": str(e)
            }
    
    def _combine_results(
        self,
        search_results: Dict[str, Any],
        crawl_results: Dict[str, Any]
    ) -> str:
        """合并搜索和爬虫结果"""
        combined = "## 搜索结果\n"
        
        for query, result in search_results.items():
            combined += f"\n### {query}\n"
            combined += result.get("result", "")[:500]
        
        if crawl_results:
            combined += "\n\n## 网页内容\n"
            combined += crawl_results.get("result", "")[:500]
        
        return combined
    
    def batch_analysis(self, topics: List[str]) -> List[Dict[str, Any]]:
        """
        批量分析多个主题
        
        Args:
            topics: 主题列表
        
        Returns:
            所有分析结果
        """
        logger.info(f"[Orchestrator] 开始批量分析: {len(topics)} 个主题")
        
        results = []
        for topic in topics:
            result = self.research_and_report(
                topic=topic,
                search_queries=[topic, f"{topic} 研究", f"{topic} 分析"]
            )
            results.append(result)
            time.sleep(2)  # 避免API速率限制
        
        logger.info(f"[Orchestrator] 批量分析完成")
        
        return results