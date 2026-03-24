"""
常量定义
"""
from enum import Enum


class AgentType(str, Enum):
    """Agent 类型"""
    SEARCH = "search"
    CRAWLER = "crawler"
    ANALYZER = "analyzer"
    REPORTER = "reporter"


class TaskStatus(str, Enum):
    """任务状态"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class SearchEngine(str, Enum):
    """搜索引擎"""
    SERPAPI = "serpapi"
    GOOGLE = "google"


# 默认配置
DEFAULT_SEARCH_ENGINE = SearchEngine.SERPAPI
DEFAULT_SEARCH_RESULTS_LIMIT = 10
DEFAULT_CRAWL_TIMEOUT = 30
DEFAULT_DATA_CHUNK_SIZE = 5000

# 提示词模板
SEARCH_AGENT_SYSTEM_PROMPT = """
你是一个专业的搜索Agent。你的职责是：
1. 根据用户的查询，使用搜索工具获取相关信息
2. 分析搜索结果的质量和相关性
3. 返回最有价值的搜索结果
4. 如果搜索不到相关信息，尝试使用不同的搜索关键词

始终确保返回的信息准确、相关且有用。
"""

CRAWLER_AGENT_SYSTEM_PROMPT = """
你是一个专业的网页爬虫Agent。你的职责是：
1. 根据提供的URL列表，爬取网页内容
2. 提取关键信息和结构化数据
3. 处理爬虫错误，进行重试
4. 返回干净的、可用的内容

始终尝试获取完整的页面内容，包括元数据。
"""

ANALYZER_AGENT_SYSTEM_PROMPT = """
你是一个数据分析专家。你的职责是：
1. 分析收集的数据和文本内容
2. 识别关键信息和模式
3. 提供深层洞察和分析结果
4. 组织数据以便报告生成

确保分析结果准确、逻辑清晰。
"""

REPORTER_AGENT_SYSTEM_PROMPT = """
你是一个报告生成专家。你的职责是：
1. 基于分析结果生成专业报告
2. 组织信息层次清晰
3. 添加摘要和建议
4. 确保报告格式规范

生成的报告应该易于阅读和理解。
"""