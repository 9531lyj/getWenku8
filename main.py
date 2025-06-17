"""
轻小说爬虫主程序
Light novel crawler main program
"""

import asyncio
import sys
import argparse
from typing import List, Optional

from utils.config import Config
from utils.logger import logger
from crawler.novel_crawler import NovelCrawler
from epub.epub_generator import EPUBGenerator

class NovelCrawlerApp:
    """小说爬虫应用程序主类"""
    
    def __init__(self):
        self.crawler = None
        self.epub_generator = EPUBGenerator()
    
    async def run(self, volume_filter: Optional[List[str]] = None):
        """运行爬虫程序"""
        try:
            logger.info("=== 轻小说爬虫程序启动 ===")
            logger.info(f"目标小说: {Config.EPUB_TITLE}")
            logger.info(f"目标URL: {Config.NOVEL_URL}")
            
            # 确保必要目录存在
            Config.ensure_directories()
            
            # 启动爬虫
            async with NovelCrawler() as crawler:
                self.crawler = crawler
                
                # 获取卷册列表
                volumes = await crawler.crawl_volume_list()
                
                # 应用卷册过滤器
                if volume_filter:
                    volumes = self._filter_volumes(volumes, volume_filter)
                    logger.info(f"应用过滤器后，将爬取 {len(volumes)} 个卷册")
                
                if not volumes:
                    logger.warning("没有找到要爬取的卷册")
                    return
                
                # 爬取所有卷册
                volumes_data = []
                for i, volume in enumerate(volumes, 1):
                    logger.info(f"开始爬取第 {i}/{len(volumes)} 个卷册: {volume['title']}")
                    
                    try:
                        volume_data = await crawler.crawl_volume(volume)
                        volumes_data.append(volume_data)
                        
                        # 立即生成EPUB（避免内存占用过多）
                        epub_path = self.epub_generator.create_epub(volume_data)
                        logger.info(f"卷册 {volume['title']} 处理完成，EPUB已保存: {epub_path}")
                        
                    except Exception as e:
                        logger.error(f"卷册 {volume['title']} 处理失败: {str(e)}")
                        continue
                
                logger.info("=== 所有卷册处理完成 ===")
                logger.info(f"成功处理 {len(volumes_data)} 个卷册")
                logger.info(f"EPUB文件保存在: {Config.OUTPUT_DIR}")
                
        except KeyboardInterrupt:
            logger.info("用户中断程序")
        except Exception as e:
            logger.error(f"程序运行出错: {str(e)}")
            raise
    
    def _filter_volumes(self, volumes: List[dict], volume_filter: List[str]) -> List[dict]:
        """根据过滤条件筛选卷册"""
        filtered_volumes = []
        
        for volume in volumes:
            volume_title = volume['title']
            
            # 检查是否匹配过滤条件
            for filter_term in volume_filter:
                if filter_term.lower() in volume_title.lower():
                    filtered_volumes.append(volume)
                    break
        
        return filtered_volumes
    
    async def test_connection(self):
        """测试网络连接"""
        logger.info("测试网络连接...")
        
        try:
            async with NovelCrawler() as crawler:
                # 尝试访问主页
                content = await crawler.get_page_content(Config.NOVEL_URL)
                if content and len(content) > 1000:
                    logger.info("网络连接正常")
                    return True
                else:
                    logger.error("网络连接异常：页面内容为空或过短")
                    return False
                    
        except Exception as e:
            logger.error(f"网络连接测试失败: {str(e)}")
            return False

def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description="轻小说《我的青春恋爱物语果然有问题》爬虫程序")
    
    parser.add_argument(
        '--volumes', '-v',
        nargs='*',
        help='指定要爬取的卷册（支持部分匹配），例如：--volumes "第一卷" "第二卷"'
    )
    
    parser.add_argument(
        '--test', '-t',
        action='store_true',
        help='仅测试网络连接，不进行爬取'
    )
    
    parser.add_argument(
        '--config',
        help='指定配置文件路径（暂未实现）'
    )
    
    return parser.parse_args()

async def main():
    """主函数"""
    args = parse_arguments()
    app = NovelCrawlerApp()
    
    if args.test:
        # 仅测试连接
        success = await app.test_connection()
        sys.exit(0 if success else 1)
    else:
        # 运行爬虫
        await app.run(volume_filter=args.volumes)

if __name__ == "__main__":
    try:
        # 设置事件循环策略（Windows兼容性）
        if sys.platform.startswith('win'):
            asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
        
        # 运行主程序
        asyncio.run(main())
        
    except KeyboardInterrupt:
        logger.info("程序被用户中断")
    except Exception as e:
        logger.error(f"程序异常退出: {str(e)}")
        sys.exit(1)
