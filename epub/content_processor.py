"""
内容处理器模块
Content processor module for intelligent text formatting
"""

import re
from typing import List, Tuple

class ContentProcessor:
    """智能内容处理器"""
    
    def __init__(self):
        # 对话识别模式
        self.dialogue_patterns = [
            r'「[^」]*」',  # 日式引号
            r'"[^"]*"',    # 英式引号
            r'"[^"]*"',    # 中文引号
            r'『[^』]*』',  # 书名号作为引号
        ]
        
        # 内心独白模式
        self.thought_patterns = [
            r'（[^）]*）',  # 中文括号
            r'\([^)]*\)',  # 英文括号
            r'——[^——]*——', # 破折号
            r'…[^…]*…',   # 省略号
        ]
        
        # 旁白/注释模式
        self.narrator_patterns = [
            r'※[^※]*※?',  # 星号
            r'＊[^＊]*＊?', # 全角星号
            r'★[^★]*★?',  # 实心星
            r'☆[^☆]*☆?',  # 空心星
            r'\[[^\]]*\]', # 方括号
        ]
        
        # 强调文本模式
        self.emphasis_patterns = [
            r'\*\*([^*]+)\*\*',  # **粗体**
            r'\*([^*]+)\*',      # *斜体*
            r'__([^_]+)__',      # __下划线__
            r'_([^_]+)_',        # _斜体_
        ]
    
    def process_content(self, content: str) -> str:
        """处理内容，返回格式化的HTML"""
        if not content:
            return "<p>内容为空</p>"
        
        # 分割段落
        paragraphs = self._split_paragraphs(content)
        
        # 处理每个段落
        html_paragraphs = []
        for para in paragraphs:
            if para.strip():
                processed_para = self._process_paragraph(para.strip())
                html_paragraphs.append(processed_para)
        
        return '\n'.join(html_paragraphs)
    
    def _split_paragraphs(self, content: str) -> List[str]:
        """智能分割段落"""
        # 先按双换行符分割
        paragraphs = content.split('\n\n')
        
        # 进一步处理单换行符的情况
        result = []
        for para in paragraphs:
            # 如果段落很长且包含单换行符，可能需要进一步分割
            if len(para) > 200 and '\n' in para:
                # 按句号、问号、感叹号后的换行符分割
                sub_paras = re.split(r'([。！？])\n', para)
                current_para = ""
                
                for i, part in enumerate(sub_paras):
                    if part in ['。', '！', '？']:
                        current_para += part
                        if len(current_para) > 50:  # 如果段落足够长，就分割
                            result.append(current_para)
                            current_para = ""
                    else:
                        current_para += part
                
                if current_para.strip():
                    result.append(current_para)
            else:
                result.append(para)
        
        return result
    
    def _process_paragraph(self, paragraph: str) -> str:
        """处理单个段落"""
        # 转义HTML字符
        escaped_para = self._escape_html(paragraph)
        
        # 应用强调格式
        escaped_para = self._apply_emphasis(escaped_para)
        
        # 识别段落类型并应用相应的CSS类
        para_type = self._identify_paragraph_type(paragraph)
        
        if para_type == 'dialogue':
            return f'    <p class="dialogue">{escaped_para}</p>'
        elif para_type == 'thought':
            return f'    <p class="thought">{escaped_para}</p>'
        elif para_type == 'narrator':
            return f'    <p class="narrator">{escaped_para}</p>'
        elif para_type == 'title':
            return f'    <h2>{escaped_para}</h2>'
        else:
            return f'    <p>{escaped_para}</p>'
    
    def _identify_paragraph_type(self, paragraph: str) -> str:
        """识别段落类型"""
        # 检查是否为小标题
        if self._is_subtitle(paragraph):
            return 'title'
        
        # 检查是否为对话
        if self._contains_pattern(paragraph, self.dialogue_patterns):
            return 'dialogue'
        
        # 检查是否为内心独白
        if self._contains_pattern(paragraph, self.thought_patterns):
            return 'thought'
        
        # 检查是否为旁白
        if self._contains_pattern(paragraph, self.narrator_patterns):
            return 'narrator'
        
        return 'normal'
    
    def _is_subtitle(self, paragraph: str) -> bool:
        """判断是否为小标题"""
        # 小标题通常较短且可能包含数字、特殊符号
        if len(paragraph) > 50:
            return False
        
        subtitle_patterns = [
            r'^\d+[、.]',  # 以数字开头
            r'^[一二三四五六七八九十]+[、.]',  # 以中文数字开头
            r'^第[一二三四五六七八九十\d]+[章节部分]',  # 章节标题
            r'^\*+\s*\w+\s*\*+$',  # 星号包围
            r'^=+\s*\w+\s*=+$',   # 等号包围
        ]
        
        return any(re.match(pattern, paragraph) for pattern in subtitle_patterns)
    
    def _contains_pattern(self, text: str, patterns: List[str]) -> bool:
        """检查文本是否包含指定模式"""
        for pattern in patterns:
            if re.search(pattern, text):
                return True
        return False
    
    def _apply_emphasis(self, text: str) -> str:
        """应用强调格式"""
        # 处理粗体
        text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
        text = re.sub(r'__([^_]+)__', r'<strong>\1</strong>', text)
        
        # 处理斜体
        text = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', text)
        text = re.sub(r'_([^_]+)_', r'<em>\1</em>', text)
        
        # 处理特殊强调（如书名、专有名词等）
        text = re.sub(r'《([^》]+)》', r'<em class="book-title">《\1》</em>', text)
        text = re.sub(r'【([^】]+)】', r'<strong class="special">\1</strong>', text)
        
        return text
    
    def _escape_html(self, text: str) -> str:
        """转义HTML特殊字符"""
        if not text:
            return ""
        
        # 基本HTML转义
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')
        text = text.replace('"', '&quot;')
        text = text.replace("'", '&#x27;')
        
        return text
    
    def create_chapter_html(self, title: str, content: str) -> str:
        """创建完整的章节HTML"""
        escaped_title = self._escape_html(title)
        processed_content = self.process_content(content)
        
        html_template = f"""<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <title>{escaped_title}</title>
    <meta charset="utf-8"/>
    <link rel="stylesheet" type="text/css" href="style/main.css"/>
</head>
<body>
    <h1>{escaped_title}</h1>
    <div class="chapter-separator">※ ※ ※</div>
{processed_content}
    <div class="chapter-separator">※ ※ ※</div>
</body>
</html>"""
        
        return html_template
    
    def create_illustration_html(self, title: str, images: List[Tuple[str, str]]) -> str:
        """创建插图页面HTML"""
        escaped_title = self._escape_html(title)
        
        # 生成图片HTML
        images_html = []
        for i, (epub_path, caption) in enumerate(images, 1):
            escaped_caption = self._escape_html(caption)
            images_html.append(f"""
    <div class="illustration">
        <img src="{epub_path}" alt="插图 {i}" />
        <div class="illustration-caption">{escaped_caption}</div>
    </div>""")
        
        html_template = f"""<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <title>{escaped_title}</title>
    <meta charset="utf-8"/>
    <link rel="stylesheet" type="text/css" href="style/main.css"/>
</head>
<body>
    <h1>{escaped_title}</h1>
    <div class="chapter-separator">※ ※ ※</div>
{''.join(images_html)}
    <div class="chapter-separator">※ ※ ※</div>
</body>
</html>"""
        
        return html_template
