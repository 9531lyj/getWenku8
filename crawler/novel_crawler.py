"""
小说爬虫核心模块
Novel crawler core module
"""

import asyncio
import os
from typing import List, Dict, Optional
from playwright.async_api import async_playwright, Browser, Page
from urllib.parse import urljoin

from utils.config import Config
from utils.logger import logger
from crawler.anti_crawler import AntiCrawlerStrategy
from crawler.page_parser import PageParser

class NovelCrawler:
    """小说爬虫主类"""
    
    def __init__(self):
        self.anti_crawler = AntiCrawlerStrategy()
        self.parser = PageParser()
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
    
    async def __aenter__(self):
        """异步上下文管理器入口"""
        await self.start()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器出口"""
        await self.close()
    
    async def start(self):
        """启动浏览器"""
        logger.info("启动浏览器...")
        playwright = await async_playwright().start()
        
        # 启动浏览器
        self.browser = await playwright.chromium.launch(
            headless=True,  # 无头模式
            args=[
                '--no-sandbox',
                '--disable-blink-features=AutomationControlled',
                '--disable-web-security',
                '--disable-features=VizDisplayCompositor'
            ]
        )
        
        # 创建页面
        context = await self.browser.new_context(**self.anti_crawler.get_playwright_options())
        self.page = await context.new_page()
        
        # 设置超时
        self.page.set_default_timeout(Config.TIMEOUT * 1000)
        
        logger.info("浏览器启动成功")
    
    async def close(self):
        """关闭浏览器"""
        if self.browser:
            await self.browser.close()
            logger.info("浏览器已关闭")
    
    async def get_page_content(self, url: str) -> str:
        """获取页面内容"""
        async def _get_content():
            # 如果是相对URL，需要基于小说目录页面构建完整URL
            if not url.startswith('http'):
                if url.endswith('.htm'):
                    # 章节页面URL
                    full_url = f"https://www.wenku8.net/novel/1/1213/{url}"
                else:
                    full_url = urljoin(Config.BASE_URL, url)
            else:
                full_url = url

            logger.debug(f"访问页面: {full_url}")

            await self.page.goto(full_url, wait_until='networkidle')
            content = await self.page.content()
            return content

        return await self.anti_crawler.handle_request_with_retry(_get_content)
    
    async def crawl_volume_list(self) -> List[Dict]:
        """爬取卷册列表"""
        logger.info("开始爬取卷册列表...")
        
        html_content = await self.get_page_content(Config.NOVEL_URL)
        volumes = self.parser.parse_volume_list(html_content)
        
        logger.info(f"成功获取 {len(volumes)} 个卷册信息")
        return volumes
    
    async def crawl_chapter(self, chapter_url: str) -> Dict:
        """爬取单个章节"""
        logger.debug(f"爬取章节: {chapter_url}")
        
        html_content = await self.get_page_content(chapter_url)
        
        # 解析章节内容
        title = self.parser.extract_chapter_title(html_content)
        content = self.parser.parse_chapter_content(html_content)
        
        return {
            'title': title,
            'content': content,
            'url': chapter_url
        }
    
    async def crawl_images(self, image_url: str, volume_name: str) -> List[str]:
        """爬取图片页面的所有图片"""
        logger.debug(f"爬取图片页面: {image_url}")
        
        html_content = await self.get_page_content(image_url)
        image_urls = self.parser.parse_image_urls(html_content)
        
        # 下载图片
        downloaded_images = []
        for i, img_url in enumerate(image_urls):
            # 生成本地文件名
            img_filename = f"{volume_name}_image_{i+1:03d}.jpg"
            img_path = os.path.join(Config.DATA_DIR, "images", img_filename)
            
            # 下载图片
            if self.parser.download_image(img_url, img_path):
                downloaded_images.append(img_path)
        
        logger.info(f"成功下载 {len(downloaded_images)} 张图片")
        return downloaded_images
    
    async def crawl_volume(self, volume: Dict) -> Dict:
        """爬取完整卷册"""
        volume_title = volume['title']
        logger.info(f"开始爬取卷册: {volume_title}")
        
        # 爬取所有章节
        chapters_data = []
        for chapter in volume['chapters']:
            try:
                chapter_data = await self.crawl_chapter(chapter['url'])
                chapters_data.append(chapter_data)
                logger.info(f"完成章节: {chapter_data['title']}")
            except Exception as e:
                logger.error(f"章节爬取失败 {chapter['title']}: {str(e)}")
        
        # 爬取图片
        images_data = []
        for image_page in volume['images']:
            try:
                volume_safe_name = self._safe_filename(volume_title)
                images = await self.crawl_images(image_page['url'], volume_safe_name)
                images_data.extend(images)
            except Exception as e:
                logger.error(f"图片爬取失败 {image_page['title']}: {str(e)}")
        
        result = {
            'title': volume_title,
            'chapters': chapters_data,
            'images': images_data
        }
        
        logger.info(f"卷册爬取完成: {volume_title} (章节: {len(chapters_data)}, 图片: {len(images_data)})")
        return result
    
    def _safe_filename(self, filename: str) -> str:
        """生成安全的文件名"""
        # 移除或替换不安全的字符
        unsafe_chars = '<>:"/\\|?*'
        for char in unsafe_chars:
            filename = filename.replace(char, '_')
        return filename.strip()
    
    async def crawl_all_volumes(self) -> List[Dict]:
        """爬取所有卷册"""
        logger.info("开始爬取所有卷册...")
        
        # 获取卷册列表
        volumes = await self.crawl_volume_list()
        
        # 爬取每个卷册
        all_volumes_data = []
        for volume in volumes:
            try:
                volume_data = await self.crawl_volume(volume)
                all_volumes_data.append(volume_data)
            except Exception as e:
                logger.error(f"卷册爬取失败 {volume['title']}: {str(e)}")
        
        logger.info(f"所有卷册爬取完成，共 {len(all_volumes_data)} 个卷册")
        return all_volumes_data
