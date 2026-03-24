"""
数据库操作
"""
from sqlalchemy import create_engine, Column, String, DateTime, JSON, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import json
from src.config import settings
from src.logger import logger

Base = declarative_base()


class TaskRecord(Base):
    """任务记录表"""
    __tablename__ = "tasks"
    
    id = Column(String, primary_key=True)
    agent_type = Column(String)
    status = Column(String)
    input_data = Column(JSON)
    output_data = Column(JSON)
    error_message = Column(String, nullable=True)
    execution_time = Column(Float)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class SearchCache(Base):
    """搜索缓存表"""
    __tablename__ = "search_cache"
    
    id = Column(String, primary_key=True)
    query = Column(String)
    results = Column(JSON)
    engine = Column(String)
    created_at = Column(DateTime, default=datetime.now)


class Database:
    """数据库管理"""
    
    def __init__(self):
        self.engine = create_engine(settings.database_url)
        # 避免 commit 后对象属性过期，导致日志访问触发 detached 错误
        self.SessionLocal = sessionmaker(bind=self.engine, expire_on_commit=False)
        Base.metadata.create_all(self.engine)
        logger.info("数据库初始化完成")
    
    def save_task(self, task_record: TaskRecord):
        """保存任务记录"""
        try:
            session = self.SessionLocal()
            session.add(task_record)
            session.commit()
            session.close()
            logger.info(f"任务 {task_record.id} 已保存到数据库")
        except Exception as e:
            logger.error(f"保存任务失败: {str(e)}")
    
    def save_search_cache(self, query: str, results: list, engine: str):
        """保存搜索缓存"""
        try:
            import hashlib
            cache_id = hashlib.md5(f"{query}_{engine}".encode()).hexdigest()
            
            session = self.SessionLocal()
            cache = SearchCache(
                id=cache_id,
                query=query,
                results=results,
                engine=engine
            )
            session.add(cache)
            session.commit()
            session.close()
            logger.info(f"搜索缓存已保存: {cache_id}")
        except Exception as e:
            logger.error(f"保存搜索缓存失败: {str(e)}")
    
    def get_search_cache(self, query: str, engine: str):
        """获取搜索缓存"""
        try:
            import hashlib
            cache_id = hashlib.md5(f"{query}_{engine}".encode()).hexdigest()
            
            session = self.SessionLocal()
            cache = session.query(SearchCache).filter_by(id=cache_id).first()
            session.close()
            
            return cache.results if cache else None
        except Exception as e:
            logger.error(f"获取搜索缓存失败: {str(e)}")
            return None


# 全局数据库实例
db = Database()