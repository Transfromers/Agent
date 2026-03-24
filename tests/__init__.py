"""
tests 包初始化

确保测试在不同启动目录下都能稳定导入项目源码。
"""

from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROJECT_ROOT_STR = str(PROJECT_ROOT)

if PROJECT_ROOT_STR not in sys.path:
    # 将项目根目录加入导入路径，支持 `from src.xxx import ...`
    sys.path.insert(0, PROJECT_ROOT_STR)
