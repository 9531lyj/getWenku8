"""
反爬虫策略模块
Anti-crawler strategy module
"""

import random
import time
import asyncio
from typing import List
from fake_useragent import UserAgent
from utils.config import Config
from utils.logger import logger

class AntiCrawlerStrategy:
    """反爬虫策略类"""
    
    def __init__(self):
        self.ua = UserAgent()
        self.request_count = 0
        self.last_request_time = 0
    
    def get_random_user_agent(self) -> str:
        """获取随机User-Agent"""
        try:
            # 优先使用fake-useragent
            return self.ua.random
        except Exception:
            # 如果失败，使用配置中的User-Agent池
            return random.choice(Config.USER_AGENTS)
    
    def get_random_delay(self) -> float:
        """获取随机延迟时间"""
        return random.uniform(Config.MIN_DELAY, Config.MAX_DELAY)
    
    async def apply_delay(self):
        """应用延迟策略"""
        delay = self.get_random_delay()
        logger.debug(f"应用延迟: {delay:.2f}秒")
        await asyncio.sleep(delay)
    
    def should_delay(self) -> bool:
        """判断是否需要延迟"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        # 如果距离上次请求时间太短，需要延迟
        if time_since_last < Config.MIN_DELAY:
            return True
        
        # 每10个请求强制延迟一次
        if self.request_count % 10 == 0 and self.request_count > 0:
            return True
        
        return False
    
    def update_request_stats(self):
        """更新请求统计"""
        self.request_count += 1
        self.last_request_time = time.time()
        
        if self.request_count % 50 == 0:
            logger.info(f"已完成 {self.request_count} 个请求")
    
    def get_playwright_options(self) -> dict:
        """获取Playwright配置选项"""
        return {
            'user_agent': self.get_random_user_agent(),
            'viewport': {'width': 1920, 'height': 1080},
            'extra_http_headers': {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }
        }
    
    async def handle_request_with_retry(self, request_func, *args, max_retries: int = None, **kwargs):
        """带重试机制的请求处理"""
        if max_retries is None:
            max_retries = Config.MAX_RETRIES
        
        last_exception = None
        
        for attempt in range(max_retries + 1):
            try:
                # 应用延迟策略
                if self.should_delay() or attempt > 0:
                    await self.apply_delay()
                
                # 执行请求
                result = await request_func(*args, **kwargs)
                
                # 更新统计
                self.update_request_stats()
                
                return result
                
            except Exception as e:
                last_exception = e
                logger.warning(f"请求失败 (尝试 {attempt + 1}/{max_retries + 1}): {str(e)}")
                
                if attempt < max_retries:
                    # 指数退避延迟
                    backoff_delay = (2 ** attempt) * Config.MIN_DELAY
                    logger.info(f"等待 {backoff_delay:.2f}秒 后重试...")
                    await asyncio.sleep(backoff_delay)
        
        # 所有重试都失败了
        logger.error(f"请求最终失败，已重试 {max_retries} 次")
        raise last_exception
