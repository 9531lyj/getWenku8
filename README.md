# 轻小说爬虫 - 我的青春恋爱物语果然有问题

这是一个专门用于爬取轻小说《我的青春恋爱物语果然有问题》的Python爬虫程序，能够自动抓取所有卷册内容并生成EPUB格式的电子书文件。

## 功能特点

- ✅ **完整内容抓取**：自动爬取所有卷册的章节内容和插图
- ✅ **EPUB格式输出**：每个卷册生成独立的EPUB电子书文件
- ✅ **图片资源处理**：自动下载并嵌入插图到电子书中
- ✅ **反爬虫策略**：实现随机延迟、User-Agent轮换等反爬机制
- ✅ **错误处理**：完善的重试机制和异常处理
- ✅ **进度显示**：详细的日志记录和进度提示
- ✅ **分卷处理**：支持选择性爬取特定卷册

## 技术架构

- **网页交互**：使用Playwright处理JavaScript渲染和反爬机制
- **内容解析**：使用BeautifulSoup解析HTML内容
- **EPUB生成**：使用ebooklib库生成标准EPUB文件
- **反爬策略**：随机延迟、User-Agent池、请求频率控制
- **异步处理**：全异步架构，提高爬取效率

## 安装说明

### 1. 环境要求

- Python 3.8 或更高版本
- Windows/Linux/macOS 系统

### 2. 安装依赖

```bash
# 克隆或下载项目到本地
cd PythonProject_GetFiction

# 安装Python依赖包
pip install -r requirements.txt

# 安装Playwright浏览器
playwright install chromium
```

### 3. 验证安装

```bash
# 测试网络连接
python main.py --test
```

## 使用方法

### 基本用法

```bash
# 爬取所有卷册
python main.py

# 爬取指定卷册（支持部分匹配）
python main.py --volumes "第一卷" "第二卷"

# 仅测试网络连接
python main.py --test
```

### 命令行参数

- `--volumes` / `-v`：指定要爬取的卷册，支持部分匹配
- `--test` / `-t`：仅测试网络连接，不进行实际爬取
- `--help` / `-h`：显示帮助信息

### 使用示例

```bash
# 爬取所有卷册
python main.py

# 只爬取前三卷
python main.py -v "第一卷" "第二卷" "第三卷"

# 爬取包含"特典"的卷册
python main.py -v "特典"
```

## 输出文件

程序运行后会在以下目录生成文件：

```
output/                 # EPUB文件输出目录
├── 我的青春恋爱物语果然有问题_第一卷.epub
├── 我的青春恋爱物语果然有问题_第二卷.epub
└── ...

data/                   # 临时数据目录
├── images/            # 下载的图片文件
└── ...

logs/                   # 日志文件目录
└── novel_crawler_YYYYMMDD_HHMMSS.log
```

## 配置说明

主要配置项在 `utils/config.py` 中：

```python
# 反爬虫配置
MIN_DELAY = 1.0         # 最小延迟时间（秒）
MAX_DELAY = 3.0         # 最大延迟时间（秒）
MAX_RETRIES = 3         # 最大重试次数
TIMEOUT = 30            # 请求超时时间（秒）

# EPUB配置
EPUB_TITLE = "我的青春恋爱物语果然有问题"
EPUB_AUTHOR = "渡航"
EPUB_LANGUAGE = "zh-CN"
EPUB_PUBLISHER = "小学馆"
```

## 注意事项

### 法律和道德规范

- ⚠️ **仅供学习研究**：本程序仅用于技术学习和个人研究
- ⚠️ **尊重版权**：请尊重原作者和出版社的版权
- ⚠️ **合理使用**：不要用于商业用途或大规模传播
- ⚠️ **遵守robots.txt**：程序会尊重网站的爬虫规则

### 使用建议

- 🕐 **避开高峰期**：建议在网站访问量较低的时间段运行
- 🐌 **控制频率**：程序已内置延迟机制，请勿修改为过于激进的参数
- 💾 **备份数据**：重要的EPUB文件请及时备份
- 🔍 **检查质量**：生成的EPUB文件建议用阅读器检查格式是否正确

## 故障排除

### 常见问题

1. **网络连接失败**
   ```bash
   # 测试网络连接
   python main.py --test
   ```

2. **Playwright浏览器未安装**
   ```bash
   playwright install chromium
   ```

3. **权限错误**
   - 确保有写入output和data目录的权限
   - Windows用户可能需要以管理员身份运行

4. **内存不足**
   - 程序会逐个处理卷册以减少内存占用
   - 如仍有问题，可以分批爬取

### 日志查看

程序运行时会生成详细的日志文件，位于 `logs/` 目录下。如遇问题，请查看日志文件获取详细错误信息。

## 项目结构

```
novel_crawler/
├── main.py                 # 主程序入口
├── requirements.txt        # 依赖包列表
├── README.md              # 说明文档
├── crawler/               # 爬虫核心模块
│   ├── novel_crawler.py   # 主爬虫类
│   ├── page_parser.py     # 页面解析器
│   └── anti_crawler.py    # 反爬虫策略
├── epub/                  # EPUB生成模块
│   └── epub_generator.py  # EPUB生成器
├── utils/                 # 工具模块
│   ├── config.py          # 配置管理
│   └── logger.py          # 日志记录
├── data/                  # 临时数据目录
├── output/                # EPUB输出目录
└── logs/                  # 日志文件目录
```

## 开发说明

如需修改或扩展功能，请参考以下模块：

- `crawler/novel_crawler.py`：修改爬取逻辑
- `crawler/page_parser.py`：修改内容解析规则
- `epub/epub_generator.py`：修改EPUB生成格式
- `utils/config.py`：修改配置参数

## 许可证

本项目仅供学习和研究使用，请遵守相关法律法规和网站使用条款。
