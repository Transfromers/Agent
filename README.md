# AI Agent 自动化系统 古法编程占比高达0%

一个基于 **LangChain**、**LangGraph** 和 **Firecrawl** 的企业级多Agent自动化框架。

## ✨ 核心特性

- **多Agent协作**：搜索、爬虫、分析、报告生成Agent协调工作
- **真实API集成**：SerpAPI、Google Search、Firecrawl等
- **强大的编排能力**：LangGraph支持复杂的工作流编排
- **数据持久化**：SQLite数据库存储任务和缓存
- **完整的日志系统**：详细的操作日志和错误跟踪
- **交互式模式**：支持命令行交互式使用
- **批量处理**：支持批量分析多个主题
- **错误恢复**：自动重试机制和错误处理

## 🏗️ 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                    User Input Layer                          │
│           (Interactive Mode / API Requests)                  │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼─────────────────────────────────────��──┐
│                 Agent Orchestrator                           │
│         (Multi-Agent Coordination & Workflow)                │
└────┬──────────┬──────────┬──────────┬──────────────────────┘
     │          │          │          │
┌────▼───┐ ┌───▼─────┐ ┌──▼───────┐ ┌──▼────────┐
│ Search │ │ Crawler │ │Analyzer  │ │ Reporter  │
│ Agent  │ │ Agent   │ │ Agent    │ │ Agent     │
└────┬───┘ └───┬─────┘ └──┬───────┘ └──┬────────┘
     │          │          │           │
     └──────────┼──────────┼───────────┘
                │          │
        ┌───────▼───┬───��──▼────────┐
        │   Tools   │   LangGraph   │
        │ (Search)  │  (Workflow)   │
        └───────┬───┴──────┬────────┘
                │          │
        ┌───────▼──────────▼────────┐
        │   LLM (ChatGPT/Claude)    │
        └───────┬──────────┬────────┘
                │          │
    ┌───────────▼──┐  ┌───▼──────────┐
    │   External   │  │  Database    │
    │   APIs       │  │  & Cache     │
    └──────────────┘  └──────────────┘
```

## 📦 项目结构

```
ai-agent-automation/
├── .env                          # 环境变量配置
├── .gitignore                    # Git忽略配置
├── requirements.txt              # 依赖包列表
├── README.md                     # 项目文档
├── main.py                       # 主程序入口
├── src/
│   ├── __init__.py
│   ├── config.py                 # 全局配置
│   ├── constants.py              # 常量定义
│   ├── logger.py                 # 日志系统
│   ├── database.py               # 数据库操作
│   ├── api/                      # 外部API集成
│   │   ├── __init__.py
│   │   ├── serpapi.py            # SerpAPI + Google Search
│   │   └── firecrawl.py          # Firecrawl网页爬虫
│   ├── tools/                    # Agent工具集
│   │   ├── __init__.py
│   │   ├── search_tools.py       # 搜索工具
│   │   ├── crawl_tools.py        # 爬虫工具
│   │   ├── data_tools.py         # 数据处理工具
│   │   └── report_tools.py       # 报告生成工具
│   ├── agents/                   # Agent定义
│   │   ├── __init__.py
│   │   ├── base_agent.py         # 基类
│   │   ├── search_agent.py       # 搜索Agent
│   │   ├── crawler_agent.py      # 爬虫Agent
│   │   ├── analyzer_agent.py     # 分析Agent
│   │   ├── reporter_agent.py     # 报告Agent
│   │   └── orchestrator.py       # Agent编排器
│   ├── models/                   # 数据模型
│   │   ├── __init__.py           # 统一导出所有模型
│   │   └── schemas.py            # Pydantic模型
│   └── utils/                    # 工具函数
│       ├── __init__.py
│       ├── validators.py         # 数据验证
│       └── helpers.py            # 辅助函数
├── logs/                         # 日志目录（自动创建）
└── tests/                        # 测试代码
    ├── __init__.py               # 做测试环境初始化
    └── test_agents.py
```

## 🚀 快速开始

### 1. 安装依赖

```bash
# 克隆项目
git clone <repo-url>
cd ai-agent-automation

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置环境变量

在项目根目录创建 `.env` 文件：

```bash
# OpenAI API
OPENAI_API_KEY=sk-your-api-key
OPENAI_MODEL=gpt-4o-mini

# SerpAPI 搜索
SERPAPI_API_KEY=your-serpapi-key

# Firecrawl 爬虫
FIRECRAWL_API_KEY=your-firecrawl-key

# Google Search (可选)
GOOGLE_API_KEY=your-google-api-key
GOOGLE_SEARCH_ENGINE_ID=your-search-engine-id

# 应用配置
APP_ENV=development
DEBUG=true
```

### 3. 运行应用

```bash
# 运行所有示例
python main.py

# 运行特定示例
python main.py example1      # 简单搜索
python main.py example2      # 搜索+爬虫
python main.py example3      # 批量分析
python main.py example4      # 自定义工作流

# 交互式模式
python main.py interactive
```

## 💡 使用示例

### Python API 使用

```python
from src.agents.orchestrator import AgentOrchestrator

# 创建编排器
orchestrator = AgentOrchestrator()

# 执行完整的研究和报告流程
result = orchestrator.research_and_report(
    topic="人工智能技术",
    search_queries=[
        "AI 最新发展",
        "深度学习应用",
        "自然语言处理"
    ],
    crawl_urls=[
        "https://openai.com",
        "https://www.anthropic.com"
    ]
)

print(result)
```

### 交互式模式命令

```bash
# 搜索
> search 人工智能应用

# 爬取网页
> crawl https://example.com https://github.com

# 分析文本
> analyze 这是一段需要分析的文本内容

# 生成报告
> report "AI技术发展" "人工智能在医疗中的应用是..."

# 完整研究流程
> research 区块链技术

# 批量分析
> batch 机器学习 自然语言处理 计算机视觉

# 退出
> exit
```

## 🔧 Agent 功能说明

### SearchAgent（搜索Agent）
- **功能**：使用SerpAPI或Google Search执行网络搜索
- **工具**：
  - `search_information` - 单个查询搜索
  - `search_multiple_queries` - 多个查询批量搜索

### CrawlerAgent（爬虫Agent）
- **功能**：使用Firecrawl爬取网页内容
- **工具**：
  - `crawl_webpage` - 爬取单个URL
  - `crawl_multiple_urls` - 批量爬取多个URL

### AnalyzerAgent（分析Agent）
- **功能**：对文本和数据进行分析
- **工具**：
  - `process_text_data` - 文本处理（摘要/提取/分析/清理）
  - `extract_key_information` - 关键信息提取

### ReporterAgent（报告Agent）
- **功能**：生成专业的分析报告
- **工具**：
  - `generate_report` - 生成完整报告
  - `format_findings` - 格式化发现和建议

## 📊 工作流示例

### 研究和报告流程
```
用户输入主题
    ↓
[搜索Agent] 搜索相关信息
    ↓
[爬虫Agent] 爬取网页内容
    ↓
[分析Agent] 分析收集的数据
    ↓
[报告Agent] 生成最终报告
    ↓
返回结果
```

## 🗄️ 数据库

项目使用SQLite数据库存储：
- **tasks** 表：任务执行记录
- **search_cache** 表：搜索结果缓存

数据库文件自动创建：`agent_automation.db`

## 📝 日志

日志文件保存在 `logs/` 目录：
- `ai-agent-automation.log` - 应用日志
- 按文件大小自动轮转（10MB）

## 🔐 安全建议

1. 不要在代码中硬编码API密钥
2. 使用环境变量或密钥管理服务
3. 在生产环境中使用HTTPS
4. 定期更新依赖包
5. 限制API调用频率

## 🛠️ 故障排除

### 导入错误
```bash
# 确保在虚拟环境中安装了所有依赖
pip install -r requirements.txt
```

### API 错误
```bash
# 检查 .env 文件中的API密钥是否正确
# 检查网络连接
# 检查API配额是否充足
```

### 数据库错误
```bash
# 删除旧数据库文件并重新初始化
rm agent_automation.db
python main.py
```

## 📚 相关文档

- [LangChain 文档](https://docs.langchain.com/)
- [LangGraph 文档](https://langchain-ai.github.io/langgraph/)
- [SerpAPI 文档](https://serpapi.com/docs)
- [Firecrawl 文档](https://docs.firecrawl.dev/)

## 

欢迎提交Issue和Pull Request！

## 📄 没有许可证

MIT License

##  zzztrans

创建于 2026-03-24

---

**⭐ 希望对你有帮助**
