"""
全局配置文件
"""
from pydantic_settings import BaseSettings
from functools import lru_cache
import os


class Settings(BaseSettings):
    """应用配置"""
    
    # API 密钥
    openai_api_key: str
    openai_model: str = "gpt-4o-mini"
    openai_base_url: str | None = None
    qwen_api_key: str | None = None
    qwen_base_url: str | None = None
    qwen_model: str = "qwen-vl-plus-2025-05-07"
    serpapi_api_key: str
    firecrawl_api_key: str
    google_api_key: str | None = None
    google_search_engine_id: str | None = None
    
    # 应用配置
    app_name: str = "AI Agent Automation"
    app_version: str = "1.0.0"
    app_env: str = "development"
    debug: bool = True
    
    # Agent 配置
    max_iterations: int = 20
    max_retries: int = 3
    timeout: int = 30
    
    # 数据库配置
    database_url: str = "sqlite:///./agent_automation.db"
    
    # 日志配置
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "allow"


@lru_cache()
def get_settings() -> Settings:
    """获取配置实例"""
    return Settings()


settings = get_settings()