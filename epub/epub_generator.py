"""
EPUB生成器模块
EPUB generator module
"""

import os
import uuid
from typing import List, Dict
from ebooklib import epub
from utils.config import Config
from utils.logger import logger
from epub.enhanced_styles import EnhancedStyles
from epub.content_processor import ContentProcessor

class EPUBGenerator:
    """EPUB文件生成器"""
    
    def __init__(self):
        self.book = None
        self.content_processor = ContentProcessor()
    
    def create_epub(self, volume_data: Dict) -> str:
        """创建EPUB文件"""
        volume_title = volume_data['title']
        logger.info(f"开始生成EPUB: {volume_title}")

        # 创建EPUB书籍对象
        self.book = epub.EpubBook()

        # 设置元数据
        self._set_metadata(volume_title)

        # 添加CSS样式
        self._add_styles()

        # 添加图片并获取图片映射
        image_mapping = self._add_images(volume_data['images'])

        # 创建插图页面
        illustration_chapters = self._create_illustration_pages(image_mapping, volume_title)

        # 添加章节
        text_chapters = self._add_chapters(volume_data['chapters'])

        # 合并所有章节（插图页面 + 文本章节）
        all_chapters = illustration_chapters + text_chapters

        if not all_chapters:
            raise ValueError("没有有效的章节内容")

        # 创建目录
        self._create_toc(all_chapters)

        # 添加导航文件
        self._add_navigation(all_chapters)

        # 生成文件
        output_path = Config.get_output_path(self._safe_filename(volume_title))

        try:
            epub.write_epub(output_path, self.book, {})
            logger.info(f"EPUB生成完成: {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"EPUB写入失败: {str(e)}")
            raise
    
    def _set_metadata(self, volume_title: str):
        """设置EPUB元数据"""
        # 设置标识符
        self.book.set_identifier(str(uuid.uuid4()))
        
        # 设置标题
        full_title = f"{Config.EPUB_TITLE} - {volume_title}"
        self.book.set_title(full_title)
        
        # 设置作者
        self.book.add_author(Config.EPUB_AUTHOR)
        
        # 设置语言
        self.book.set_language(Config.EPUB_LANGUAGE)
        
        # 设置出版商
        self.book.add_metadata('DC', 'publisher', Config.EPUB_PUBLISHER)
        
        # 设置描述
        description = f"轻小说《{Config.EPUB_TITLE}》{volume_title}，作者：{Config.EPUB_AUTHOR}"
        self.book.add_metadata('DC', 'description', description)

    def _add_styles(self):
        """添加CSS样式"""
        # 主要样式文件
        main_css = epub.EpubItem(
            uid="main_css",
            file_name="style/main.css",
            media_type="text/css",
            content=EnhancedStyles.get_main_css()
        )
        self.book.add_item(main_css)

        # 导航样式文件
        nav_css = epub.EpubItem(
            uid="nav_css",
            file_name="style/nav.css",
            media_type="text/css",
            content=EnhancedStyles.get_navigation_css()
        )
        self.book.add_item(nav_css)
    
    def _add_chapters(self, chapters_data: List[Dict]) -> List[epub.EpubHtml]:
        """添加章节到EPUB"""
        epub_chapters = []

        for i, chapter_data in enumerate(chapters_data):
            chapter_title = chapter_data['title']
            chapter_content = chapter_data['content']

            # 检查章节内容是否为空
            if not chapter_content or len(chapter_content.strip()) < 10:
                logger.warning(f"章节内容为空或过短，跳过: {chapter_title}")
                continue

            # 创建章节文件名
            chapter_filename = f"chapter_{i+1:03d}.xhtml"

            # 创建EPUB章节
            chapter = epub.EpubHtml(
                title=chapter_title,
                file_name=chapter_filename,
                lang=Config.EPUB_LANGUAGE
            )

            # 设置章节内容
            html_content = self.content_processor.create_chapter_html(chapter_title, chapter_content)
            chapter.content = html_content

            # 添加CSS样式引用
            chapter.add_item(self.book.get_item_with_id("main_css"))

            # 添加到书籍
            self.book.add_item(chapter)
            epub_chapters.append(chapter)

            logger.debug(f"添加章节: {chapter_title} (内容长度: {len(chapter_content)})")

        return epub_chapters
    
    def _add_images(self, image_paths: List[str]) -> Dict[str, str]:
        """添加图片到EPUB并返回图片映射"""
        image_mapping = {}

        for i, image_path in enumerate(image_paths):
            if os.path.exists(image_path):
                try:
                    # 读取图片文件
                    with open(image_path, 'rb') as img_file:
                        img_content = img_file.read()

                    # 获取文件名
                    img_filename = os.path.basename(image_path)
                    epub_img_path = f"images/{img_filename}"

                    # 创建EPUB图片项
                    img_item = epub.EpubItem(
                        uid=f"img_{i+1:03d}",
                        file_name=epub_img_path,
                        media_type="image/jpeg",
                        content=img_content
                    )

                    # 添加到书籍
                    self.book.add_item(img_item)

                    # 添加到映射
                    image_mapping[image_path] = epub_img_path

                    logger.debug(f"添加图片: {img_filename}")

                except Exception as e:
                    logger.error(f"添加图片失败 {image_path}: {str(e)}")

        return image_mapping

    def _create_illustration_pages(self, image_mapping: Dict[str, str], volume_title: str) -> List[epub.EpubHtml]:
        """创建插图页面"""
        illustration_chapters = []

        if not image_mapping:
            return illustration_chapters

        # 创建插图总页面
        illustrations_html = self._create_illustrations_overview(image_mapping, volume_title)

        illustrations_page = epub.EpubHtml(
            title=f"{volume_title} 插图",
            file_name="illustrations.xhtml",
            lang=Config.EPUB_LANGUAGE
        )
        illustrations_page.content = illustrations_html
        illustrations_page.add_item(self.book.get_item_with_id("main_css"))

        self.book.add_item(illustrations_page)
        illustration_chapters.append(illustrations_page)

        logger.info(f"创建插图页面，包含 {len(image_mapping)} 张图片")
        return illustration_chapters

    def _create_illustrations_overview(self, image_mapping: Dict[str, str], volume_title: str) -> str:
        """创建插图总览页面HTML"""
        title = f"{volume_title} 插图"

        # 准备图片数据
        images_data = []
        for i, (local_path, epub_path) in enumerate(image_mapping.items(), 1):
            img_filename = os.path.basename(local_path)
            img_name = img_filename.replace('.jpg', '').replace('_', ' ')
            caption = f"插图 {i}: {img_name}"
            images_data.append((epub_path, caption))

        return self.content_processor.create_illustration_html(title, images_data)
    

    
    def _create_toc(self, chapters: List[epub.EpubHtml]):
        """创建目录"""
        # 创建目录结构
        toc_items = []
        for chapter in chapters:
            toc_items.append(chapter)  # 直接使用章节对象

        self.book.toc = toc_items
    
    def _add_navigation(self, chapters: List[epub.EpubHtml]):
        """添加导航文件"""
        # 添加NCX和导航文档
        self.book.add_item(epub.EpubNcx())
        self.book.add_item(epub.EpubNav())

        # 设置书脊（阅读顺序）
        spine_items = ['nav']
        for chapter in chapters:
            spine_items.append(chapter)

        self.book.spine = spine_items
    
    def _safe_filename(self, filename: str) -> str:
        """生成安全的文件名"""
        unsafe_chars = '<>:"/\\|?*'
        for char in unsafe_chars:
            filename = filename.replace(char, '_')
        return filename.strip()
    
    def create_all_epubs(self, volumes_data: List[Dict]) -> List[str]:
        """为所有卷册创建EPUB文件"""
        epub_files = []
        
        for volume_data in volumes_data:
            try:
                epub_path = self.create_epub(volume_data)
                epub_files.append(epub_path)
            except Exception as e:
                logger.error(f"EPUB生成失败 {volume_data['title']}: {str(e)}")
        
        logger.info(f"共生成 {len(epub_files)} 个EPUB文件")
        return epub_files
