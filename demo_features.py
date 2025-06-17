"""
功能演示脚本
Feature demonstration script
"""

import os
from epub.epub_generator import EPUBGenerator
from utils.logger import logger

def create_demo_epub():
    """创建演示EPUB，展示所有功能"""
    
    # 创建演示数据
    demo_volume_data = {
        'title': '功能演示卷',
        'chapters': [
            {
                'title': '第一章 文本格式演示',
                'content': '''这是一个普通段落，用来展示基本的文本格式。

「这是一段对话，」主角说道，「应该会以特殊的样式显示。」

（这是内心独白，通常用括号表示。）

**这是粗体文本**，*这是斜体文本*。

《这是书名》，【这是特殊强调】。

※ 这是旁白或注释文本 ※

——这也是一种内心独白的表示方式——

这是另一个普通段落，用来测试段落间的间距和排版效果。文本应该自动对齐，并且有适当的行间距。

"这是另一种对话格式，"另一个角色回应道。

1. 这可能是一个小标题

这是小标题下的内容，应该有不同的格式。

★ 特殊标记的文本 ★

最后一个段落，用来结束这个演示章节。''',
                'url': 'demo1.htm'
            },
            {
                'title': '第二章 更多样式测试',
                'content': '''这一章继续展示更多的文本样式和格式。

「你觉得这个格式怎么样？」雪乃问道。

（看起来还不错，）八幡心想，（至少比之前的版本好多了。）

**重要提示**：这个EPUB生成器现在支持：
- 智能段落识别
- 对话格式化
- 内心独白样式
- 旁白和注释
- 图片嵌入
- 响应式设计
- 深色模式支持

*这些功能*让阅读体验更加舒适和专业。

「确实如此，」结衣附和道，「现在看起来就像真正的电子书了。」

※ 作者注：这个演示展示了各种文本格式的处理能力 ※

__下划线强调__也是支持的格式之一。

《轻小说爬虫项目》现在已经具备了完整的功能。

最终段落：感谢您使用这个爬虫程序！''',
                'url': 'demo2.htm'
            }
        ],
        'images': []  # 演示版本不包含图片
    }
    
    try:
        generator = EPUBGenerator()
        epub_path = generator.create_epub(demo_volume_data)
        logger.info(f"演示EPUB生成成功: {epub_path}")
        
        print("\n" + "="*60)
        print("🎉 功能演示EPUB生成成功！")
        print("="*60)
        print(f"📁 文件位置: {epub_path}")
        print("\n📖 新功能特性:")
        print("✅ 智能文本格式识别")
        print("✅ 对话样式优化")
        print("✅ 内心独白格式")
        print("✅ 旁白和注释样式")
        print("✅ 强调文本处理")
        print("✅ 专业CSS样式")
        print("✅ 响应式设计")
        print("✅ 深色模式支持")
        print("✅ 图片嵌入功能")
        print("✅ 优雅的排版")
        print("\n🔍 建议使用电子书阅读器打开查看效果")
        print("推荐阅读器: Calibre, Adobe Digital Editions, Apple Books")
        
        return True
    except Exception as e:
        logger.error(f"演示EPUB生成失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def show_file_structure():
    """显示项目文件结构"""
    print("\n" + "="*60)
    print("📁 项目文件结构")
    print("="*60)
    
    structure = """
PythonProject_GetFiction/
├── 📄 main.py                     # 主程序入口
├── 📄 install.py                  # 安装脚本
├── 📄 test_epub.py               # EPUB测试脚本
├── 📄 demo_features.py           # 功能演示脚本
├── 📄 requirements.txt           # 依赖包列表
├── 📄 README.md                  # 项目说明
├── 📄 使用指南.md                # 中文使用指南
├── 📁 crawler/                   # 爬虫核心模块
│   ├── 📄 novel_crawler.py       # 主爬虫类
│   ├── 📄 page_parser.py         # 页面解析器
│   └── 📄 anti_crawler.py        # 反爬虫策略
├── 📁 epub/                      # EPUB生成模块
│   ├── 📄 epub_generator.py      # EPUB生成器
│   ├── 📄 enhanced_styles.py     # 增强样式
│   └── 📄 content_processor.py   # 内容处理器
├── 📁 utils/                     # 工具模块
│   ├── 📄 config.py              # 配置管理
│   └── 📄 logger.py              # 日志记录
├── 📁 output/                    # EPUB输出目录
│   ├── 📚 我的青春恋爱物语果然有问题_第一卷.epub
│   └── 📚 功能演示卷.epub
├── 📁 data/images/               # 下载的图片
└── 📁 logs/                      # 日志文件
"""
    
    print(structure)

def show_usage_examples():
    """显示使用示例"""
    print("\n" + "="*60)
    print("🚀 使用示例")
    print("="*60)
    
    examples = """
# 基本使用
python main.py                              # 爬取所有卷册
python main.py --test                       # 测试网络连接
python main.py --volumes "第一卷"           # 爬取指定卷册

# 批量爬取
python main.py -v "第一卷" "第二卷" "第三卷"  # 爬取多个卷册
python main.py -v "第6.5卷" "第7.5卷"       # 爬取特典卷册

# 功能测试
python test_epub.py                         # 测试EPUB生成
python demo_features.py                     # 生成功能演示

# 安装和设置
python install.py                           # 自动安装依赖
pip install -r requirements.txt             # 手动安装依赖
playwright install chromium                 # 安装浏览器
"""
    
    print(examples)

def main():
    """主函数"""
    print("🎨 轻小说爬虫 - 功能演示")
    print("="*60)
    
    # 显示项目结构
    show_file_structure()
    
    # 显示使用示例
    show_usage_examples()
    
    # 询问是否生成演示EPUB
    try:
        response = input("\n是否生成功能演示EPUB文件? (y/n): ").lower().strip()
        if response in ['y', 'yes', '是', '1']:
            create_demo_epub()
        else:
            print("跳过演示EPUB生成")
    except KeyboardInterrupt:
        print("\n\n程序被用户中断")
    
    print("\n" + "="*60)
    print("📚 感谢使用轻小说爬虫程序！")
    print("="*60)
    print("🔗 项目特色:")
    print("   • 完整的轻小说内容抓取")
    print("   • 专业的EPUB电子书生成")
    print("   • 智能的文本格式处理")
    print("   • 优雅的阅读样式设计")
    print("   • 完善的反爬虫策略")
    print("   • 详细的日志记录")
    print("\n⚠️  请遵守相关法律法规，仅供学习研究使用")

if __name__ == "__main__":
    main()
