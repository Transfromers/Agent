"""
Agent 基类
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from src.config import settings
from src.logger import logger
from src.constants import AgentType


class BaseAgent(ABC):
    """Agent 基类"""
    
    def __init__(
        self,
        agent_type: str,
        name: str,
        system_prompt: str,
        tools: List[Any]
    ):
        """
        初始化Agent
        
        Args:
            agent_type: Agent类型
            name: Agent名称
            system_prompt: 系统提示词
            tools: 可用工具列表
        """
        self.agent_type = agent_type
        self.name = name
        self.system_prompt = system_prompt
        self.tools = tools

        # 初始化LLM（优先使用 Qwen 兼容配置，其次是 OpenAI 配置）
        api_key, base_url, provider, model_name = self._resolve_llm_config()
        llm_kwargs = {
            "model": model_name,
            "temperature": 0,
            "api_key": api_key,
        }
        if base_url:
            llm_kwargs["base_url"] = base_url

        self.llm = ChatOpenAI(**llm_kwargs)
        
        # 绑定工具到LLM
        self.llm_with_tools = self.llm.bind_tools(tools) if tools else self.llm
        
        logger.info(f"Agent '{self.name}' 初始化完成，LLM提供方: {provider}，模型: {model_name}")

    def _resolve_llm_config(self):
        """解析LLM连接配置，兼容Qwen/OpenAI。"""
        preferred_model = settings.openai_model

        # 允许直接用 OPENAI_* 指向兼容端点
        if settings.openai_api_key and settings.openai_base_url:
            return (
                settings.openai_api_key,
                settings.openai_base_url,
                "openai_compatible",
                preferred_model,
            )

        # 若设置了 Qwen 专用变量，优先使用
        if settings.qwen_api_key and settings.qwen_base_url:
            # 在Qwen通道下，若仍是OpenAI默认模型，则自动切换到Qwen默认模型
            if preferred_model == "gpt-4o-mini":
                preferred_model = settings.qwen_model
            return (
                settings.qwen_api_key,
                settings.qwen_base_url,
                "qwen_compatible",
                preferred_model,
            )

        # 兼容默认 OpenAI 直连
        return settings.openai_api_key, None, "openai_default", preferred_model
    
    def create_graph(self):
        """创建LangGraph工作流"""
        workflow = StateGraph(dict)
        
        # 添加节点
        workflow.add_node("agent", self._agent_node)
        if self.tools:
            workflow.add_node("tools", self._tools_node)
        
        # 设置入口
        workflow.add_edge(START, "agent")
        
        # 添加条件边
        if self.tools:
            workflow.add_conditional_edges(
                "agent",
                self._should_continue,
                {
                    "tools": "tools",
                    "end": END
                }
            )
            workflow.add_edge("tools", "agent")
        else:
            workflow.add_edge("agent", END)
        
        # 编译图
        self.graph = workflow.compile()
        
        return self.graph
    
    def _agent_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Agent 决策节点"""
        messages = state.get("messages", [])
        
        logger.info(f"[{self.name}] 处理消息，消息数: {len(messages)}")
        
        # 调用LLM
        response = self.llm_with_tools.invoke(messages)
        
        return {"messages": messages + [response]}
    
    def _tools_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """工具执行节点"""
        messages = state.get("messages", [])
        
        if not messages:
            return {"messages": []}
        
        last_message = messages[-1]
        
        # 执行工具调用
        tool_node = ToolNode(self.tools)
        tool_results = tool_node.invoke({"messages": [last_message]})
        
        logger.info(f"[{self.name}] 工具执行完成")
        
        return tool_results
    
    def _should_continue(self, state: Dict[str, Any]) -> str:
        """判断是否继续执行"""
        messages = state.get("messages", [])
        
        if not messages:
            return "end"
        
        last_message = messages[-1]
        
        # 如果有工具调用，继续执行
        if hasattr(last_message, "tool_calls") and last_message.tool_calls:
            return "tools"
        
        return "end"
    
    def run(self, user_input: str, max_iterations: int = 10) -> str:
        """
        运行Agent
        
        Args:
            user_input: 用户输入
            max_iterations: 最大迭代次数
        
        Returns:
            执行结果
        """
        logger.info(f"[{self.name}] 开始执行，输入: {user_input}")
        
        # 创建图
        self.create_graph()
        
        # 初始状态
        initial_state = {
            "messages": [{"role": "user", "content": user_input}]
        }
        
        try:
            # 执行图
            final_state = self.graph.invoke(
                initial_state,
                config={"recursion_limit": max_iterations}
            )
            
            # 提取结果
            messages = final_state.get("messages", [])
            if messages:
                last_message = messages[-1]
                result = getattr(last_message, "content", str(last_message))
                logger.info(f"[{self.name}] 执行成功")
                return result
            
            return "执行完成，但未获得结果"
        
        except Exception as e:
            logger.error(f"[{self.name}] 执行失败: {str(e)}")
            return f"执行错误: {str(e)}"