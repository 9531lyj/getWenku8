"""
测试EPUB生成功能
"""

from epub.epub_generator import EPUBGenerator
from utils.logger import logger

def test_epub_generation():
    """测试EPUB生成"""
    
    # 创建测试数据
    test_volume_data = {
        'title': '测试卷册',
        'chapters': [
            {
                'title': '第一章 测试章节',
                'content': '这是一个测试章节的内容。\n\n这里是第二段内容。\n\n这里是第三段内容，用来测试EPUB生成功能是否正常工作。',
                'url': 'test1.htm'
            },
            {
                'title': '第二章 另一个测试章节',
                'content': '这是第二个测试章节。\n\n包含多段文字内容。\n\n用于验证EPUB格式是否正确。',
                'url': 'test2.htm'
            }
        ],
        'images': []  # 暂时不测试图片
    }
    
    try:
        generator = EPUBGenerator()
        epub_path = generator.create_epub(test_volume_data)
        logger.info(f"测试EPUB生成成功: {epub_path}")
        return True
    except Exception as e:
        logger.error(f"测试EPUB生成失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_epub_generation()
