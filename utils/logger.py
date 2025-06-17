"""
日志记录模块
Logging module
"""

import logging
import os
from datetime import datetime
from typing import Optional

class Logger:
    """日志记录器类"""
    
    _instance: Optional['Logger'] = None
    _logger: Optional[logging.Logger] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._logger is None:
            self._setup_logger()
    
    def _setup_logger(self):
        """设置日志记录器"""
        # 确保日志目录存在
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)
        
        # 创建日志文件名（包含时间戳）
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = os.path.join(log_dir, f"novel_crawler_{timestamp}.log")
        
        # 创建logger
        self._logger = logging.getLogger("NovelCrawler")
        self._logger.setLevel(logging.DEBUG)
        
        # 清除已有的处理器
        self._logger.handlers.clear()
        
        # 创建文件处理器
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        
        # 创建控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # 创建格式器
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # 添加处理器到logger
        self._logger.addHandler(file_handler)
        self._logger.addHandler(console_handler)
    
    def debug(self, message: str):
        """记录调试信息"""
        self._logger.debug(message)
    
    def info(self, message: str):
        """记录一般信息"""
        self._logger.info(message)
    
    def warning(self, message: str):
        """记录警告信息"""
        self._logger.warning(message)
    
    def error(self, message: str):
        """记录错误信息"""
        self._logger.error(message)
    
    def critical(self, message: str):
        """记录严重错误信息"""
        self._logger.critical(message)

# 创建全局logger实例
logger = Logger()
