"""
页面解析器模块
Page parser module
"""

import re
import os
import requests
from typing import List, Dict, Tuple, Optional
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from utils.config import Config
from utils.logger import logger

class PageParser:
    """页面解析器类"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def parse_volume_list(self, html_content: str) -> List[Dict]:
        """解析卷册列表"""
        soup = BeautifulSoup(html_content, 'lxml')
        volumes = []
        
        # 查找所有卷册表格
        tables = soup.find_all('table')
        
        for table in tables:
            rows = table.find_all('tr')
            current_volume = None
            
            for row in rows:
                cells = row.find_all('td')
                
                # 检查是否是卷册标题行
                if len(cells) == 1 and cells[0].get_text().strip().startswith('第'):
                    volume_title = cells[0].get_text().strip()
                    current_volume = {
                        'title': volume_title,
                        'chapters': [],
                        'images': []
                    }
                    volumes.append(current_volume)
                    logger.info(f"发现卷册: {volume_title}")
                
                # 解析章节链接
                elif current_volume and len(cells) > 0:
                    for cell in cells:
                        links = cell.find_all('a')
                        for link in links:
                            href = link.get('href')
                            title = link.get_text().strip()
                            
                            if href and title:
                                if '插图' in title:
                                    current_volume['images'].append({
                                        'title': title,
                                        'url': href
                                    })
                                else:
                                    current_volume['chapters'].append({
                                        'title': title,
                                        'url': href
                                    })
        
        logger.info(f"共发现 {len(volumes)} 个卷册")
        return volumes
    
    def parse_chapter_content(self, html_content: str) -> str:
        """解析章节内容"""
        soup = BeautifulSoup(html_content, 'lxml')

        # 移除脚本和样式标签
        for script in soup(["script", "style", "nav", "header", "footer"]):
            script.decompose()

        # 查找内容容器 - 根据实际网站结构调整
        content_div = None

        # 尝试多种可能的内容容器选择器
        selectors = [
            'div[id*="content"]',
            'div[class*="content"]',
            'div[id*="text"]',
            'div[class*="text"]',
            'div[id*="main"]',
            'div[class*="main"]'
        ]

        for selector in selectors:
            content_div = soup.select_one(selector)
            if content_div:
                break

        if not content_div:
            # 如果找不到特定容器，查找包含最多文本的div
            logger.warning("未找到内容容器，尝试提取最大文本块")

            divs = soup.find_all('div')
            max_text_length = 0
            best_div = None

            for div in divs:
                # 跳过导航和控制元素
                if div.find(['nav', 'header', 'footer', 'script', 'style']):
                    continue

                text = div.get_text().strip()
                if len(text) > max_text_length and len(text) > 500:  # 至少500字符
                    max_text_length = len(text)
                    best_div = div

            content_div = best_div

        if content_div:
            # 清理内容
            content = self._clean_content(content_div.get_text())
            if len(content) > 100:  # 确保内容不为空
                return content

        logger.error("无法解析章节内容")
        return ""
    
    def parse_image_urls(self, html_content: str) -> List[str]:
        """解析图片URL列表"""
        soup = BeautifulSoup(html_content, 'lxml')
        image_urls = []
        
        # 查找所有图片链接
        img_tags = soup.find_all('img')
        for img in img_tags:
            src = img.get('src')
            if src and 'pic.777743.xyz' in src:
                image_urls.append(src)
        
        # 也查找链接中的图片
        links = soup.find_all('a')
        for link in links:
            href = link.get('href')
            if href and href.endswith('.jpg'):
                image_urls.append(href)
        
        logger.info(f"发现 {len(image_urls)} 张图片")
        return image_urls
    
    def download_image(self, url: str, save_path: str) -> bool:
        """下载图片"""
        try:
            response = self.session.get(url, timeout=Config.TIMEOUT)
            response.raise_for_status()
            
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            
            with open(save_path, 'wb') as f:
                f.write(response.content)
            
            logger.debug(f"图片下载成功: {save_path}")
            return True
            
        except Exception as e:
            logger.error(f"图片下载失败 {url}: {str(e)}")
            return False
    
    def _clean_content(self, text: str) -> str:
        """清理文本内容"""
        if not text:
            return ""
        
        # 移除多余的空白字符
        text = re.sub(r'\s+', ' ', text)
        
        # 移除页面导航相关文本
        patterns_to_remove = [
            r'背景颜色.*?保存设置',
            r'轻小说文库.*?繁體化',
            r'添加书签.*?内容报错',
            r'添加书签.*?返回书目',
            r'绅士游戏.*?online',
        ]
        
        for pattern in patterns_to_remove:
            text = re.sub(pattern, '', text, flags=re.DOTALL)
        
        # 分割成段落并清理
        paragraphs = text.split('\n')
        cleaned_paragraphs = []
        
        for para in paragraphs:
            para = para.strip()
            if para and len(para) > 1:  # 过滤掉太短的段落
                cleaned_paragraphs.append(para)
        
        return '\n\n'.join(cleaned_paragraphs)
    
    def extract_chapter_title(self, html_content: str) -> str:
        """提取章节标题"""
        soup = BeautifulSoup(html_content, 'lxml')

        # 尝试从title标签提取
        title_tag = soup.find('title')
        if title_tag:
            title = title_tag.get_text().strip()
            # 提取章节部分 - 处理多种分隔符
            for separator in ['-', '|', '_']:
                if separator in title:
                    parts = title.split(separator)
                    for part in parts:
                        part = part.strip()
                        if ('第' in part and ('章' in part or '卷' in part)) or '序' in part or '后记' in part:
                            return part

        # 尝试从页面内容提取标题
        # 查找可能的标题元素
        title_selectors = [
            'h1', 'h2', 'h3', 'h4',
            'div[class*="title"]',
            'div[id*="title"]',
            'span[class*="title"]'
        ]

        for selector in title_selectors:
            elements = soup.select(selector)
            for element in elements:
                text = element.get_text().strip()
                if text and (('第' in text and ('章' in text or '卷' in text)) or
                           '序' in text or '后记' in text or '插图' in text):
                    return text

        # 如果都找不到，尝试从页面内容中提取第一行可能的标题
        content_text = soup.get_text()
        lines = content_text.split('\n')
        for line in lines[:10]:  # 只检查前10行
            line = line.strip()
            if line and (('第' in line and ('章' in line or '卷' in line)) or
                        '序' in line or '后记' in line):
                return line

        return "未知章节"
