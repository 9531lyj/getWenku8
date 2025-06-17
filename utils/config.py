"""
配置管理模块
Configuration management module
"""

import os
from typing import List

class Config:
    """爬虫配置类"""
    
    # 基础URL配置
    BASE_URL = "https://www.wenku8.net"
    NOVEL_URL = "https://www.wenku8.net/novel/1/1213/index.htm"
    
    # 反爬虫配置
    MIN_DELAY = 1.0  # 最小延迟时间（秒）
    MAX_DELAY = 3.0  # 最大延迟时间（秒）
    MAX_RETRIES = 3  # 最大重试次数
    TIMEOUT = 30     # 请求超时时间（秒）
    
    # User-Agent池
    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:119.0) Gecko/20100101 Firefox/119.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    ]
    
    # 文件路径配置
    DATA_DIR = "data"
    OUTPUT_DIR = "output"
    LOG_DIR = "logs"
    
    # EPUB配置
    EPUB_TITLE = "我的青春恋爱物语果然有问题"
    EPUB_AUTHOR = "渡航"
    EPUB_LANGUAGE = "zh-CN"
    EPUB_PUBLISHER = "小学馆"
    
    @classmethod
    def ensure_directories(cls):
        """确保必要的目录存在"""
        for directory in [cls.DATA_DIR, cls.OUTPUT_DIR, cls.LOG_DIR]:
            os.makedirs(directory, exist_ok=True)
    
    @classmethod
    def get_output_path(cls, volume_name: str) -> str:
        """获取输出文件路径"""
        cls.ensure_directories()
        filename = f"{cls.EPUB_TITLE}_{volume_name}.epub"
        return os.path.join(cls.OUTPUT_DIR, filename)
