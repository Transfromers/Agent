"""
主程序入口
"""
import sys
from src.agents.orchestrator import AgentOrchestrator
from src.logger import logger
import json
from datetime import datetime


def print_result(result: dict):
    """美化打印结果"""
    print("\n" + "="*80)
    print("📊 执行结果")
    print("="*80)
    
    # 处理大量数据的情况
    if isinstance(result, dict):
        simplified = {}
        for key, value in result.items():
            if isinstance(value, str) and len(value) > 200:
                simplified[key] = value[:200] + "..."
            elif isinstance(value, list):
                simplified[key] = f"[{len(value)} items]"
            else:
                simplified[key] = value
        print(json.dumps(simplified, indent=2, ensure_ascii=False))
    else:
        print(str(result))
    
    print("="*80 + "\n")


def example_1_simple_search():
    """示例1: 简单搜索"""
    print("\n" + "🔍 示例1: 简单搜索任务")
    print("-" * 80)
    
    orchestrator = AgentOrchestrator()
    
    result = orchestrator.research_and_report(
        topic="Python AI 编程",
        search_queries=[
            "Python AI 最佳实践",
            "LangChain 框架",
            "AI Agent 开发"
        ]
    )
    
    print_result(result)


def example_2_with_crawling():
    """示例2: 搜索+爬虫"""
    print("\n" + "🕷️  示例2: 搜索和爬虫任务")
    print("-" * 80)
    
    # orchestrator = AgentOrchestrator()
    
    inputs = {
        "topic": "最新AI技术动态",
        "search_queries": [
            "AI 最新发展",
            "2024年AI突破",
            "深度学习应用"
        ],
        "crawl_urls": [
            "https://example.com",
            "https://github.com"
        ]
    }
    
    result = app.invoke(inputs)
    
    print_result(result)


def example_3_batch_analysis():
    """示例3: 批量分析"""
    print("\n" + "📚 示例3: 批量分析任务")
    print("-" * 80)
    
    orchestrator = AgentOrchestrator()
    
    topics = [
        "机器学习在医疗中的应用",
        "自然语言处理技术",
        "计算机视觉最新进展"
    ]
    
    results = orchestrator.batch_analysis(topics)
    
    for i, result in enumerate(results, 1):
        print(f"\n✅ 主题 {i} 分析完成")
        print_result(result)


def example_4_custom_workflow():
    """示例4: 自定义工作流"""
    print("\n" + "⚙️  示例4: 自定义工作流")
    print("-" * 80)
    
    orchestrator = AgentOrchestrator()
    
    # 自定义工作流：只进行搜索和分析，不生成报告
    logger.info("执行自定义工作流")
    
    # 步骤1: 搜索
    search_result = orchestrator.search_agent.run(
        "区块链技术应用"
    )
    print(f"✅ 搜索完成")
    
    # 步骤2: 分析
    if search_result.get("result"):
        analysis_result = orchestrator.analyzer_agent.run(
            data=search_result.get("result"),
            analysis_type="analyze"
        )
        print(f"✅ 分析完成")
    
    print_result({
        "workflow": "custom",
        "steps": ["search", "analyze"],
        "search_result": search_result,
        "analysis_result": analysis_result if 'analysis_result' in locals() else None
    })


def interactive_mode():
    """交互式模式"""
    print("\n" + "🤖 AI Agent 自动化系统 - 交互式模式")
    print("="*80)
    print("""
可用命令:
  1. search <query>              - 搜索查询
  2. crawl <url1> <url2> ...     - 爬取URL
  3. analyze <text>              - 分析文本
  4. report <title> <content>    - 生成报告
  5. research <topic>            - 完整研究流程
  6. batch <topic1> <topic2>     - 批量分析
  7. exit                         - 退出
    """)
    print("="*80)
    
    orchestrator = AgentOrchestrator()
    
    while True:
        try:
            user_input = input("\n> ").strip()
            
            if not user_input:
                continue
            
            command_parts = user_input.split()
            command = command_parts[0].lower()
            
            if command == "exit":
                print("\n👋 再见!")
                break
            
            elif command == "search" and len(command_parts) > 1:
                query = " ".join(command_parts[1:])
                result = orchestrator.search_agent.run(query)
                print_result(result)
            
            elif command == "crawl" and len(command_parts) > 1:
                urls = command_parts[1:]
                result = orchestrator.crawler_agent.run(urls)
                print_result(result)
            
            elif command == "analyze" and len(command_parts) > 1:
                text = " ".join(command_parts[1:])
                result = orchestrator.analyzer_agent.run(text)
                print_result(result)
            
            elif command == "report" and len(command_parts) > 2:
                title = command_parts[1]
                content = " ".join(command_parts[2:])
                result = orchestrator.reporter_agent.run(
                    title=title,
                    content=content,
                    data_sources=["user_input"]
                )
                print_result(result)
            
            elif command == "research" and len(command_parts) > 1:
                topic = " ".join(command_parts[1:])
                result = orchestrator.research_and_report(
                    topic=topic,
                    search_queries=[topic, f"{topic} 分析", f"{topic} 应用"]
                )
                print_result(result)
            
            elif command == "batch" and len(command_parts) > 1:
                topics = command_parts[1:]
                results = orchestrator.batch_analysis(topics)
                for result in results:
                    print_result(result)
            
            else:
                print("❌ 未知命令或参数错误")
        
        except KeyboardInterrupt:
            print("\n\n👋 已中断")
            break
        except Exception as e:
            logger.error(f"错误: {str(e)}")
            print(f"❌ 错误: {str(e)}")


def main():
    """主函数"""
    print("""
    
╔════════════════════════════════════════════════════════════════════════════╗
║                  🤖 AI Agent 自动化系统 v1.0                               ║
║         基于 LangChain + LangGraph + Firecrawl 的多Agent框架               ║
╚════════════════════════════════════════════════════════════════════════════╝
    """)
    
    logger.info("应用启动")
    
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
        
        if mode == "example1":
            example_1_simple_search()
        elif mode == "example2":
            example_2_with_crawling()
        elif mode == "example3":
            example_3_batch_analysis()
        elif mode == "example4":
            example_4_custom_workflow()
        elif mode == "interactive":
            interactive_mode()
        else:
            print(f"未知模式: {mode}")
            print("\n用法:")
            print("  python main.py example1       - 运行示例1: 简单搜索")
            print("  python main.py example2       - 运行示例2: 搜索+爬虫")
            print("  python main.py example3       - 运行示例3: 批量分析")
            print("  python main.py example4       - 运行示例4: 自定义工作流")
            print("  python main.py interactive    - 交互式模式")
    else:
        # 默认运行所有示例
        print("\n🚀 运行所有示例...\n")
        
        try:
            example_1_simple_search()
            example_2_with_crawling()
            example_3_batch_analysis()
            example_4_custom_workflow()
        except Exception as e:
            logger.error(f"示例执行失败: {str(e)}")
            print(f"\n❌ 执行失败: {str(e)}")


if __name__ == "__main__":
    main()