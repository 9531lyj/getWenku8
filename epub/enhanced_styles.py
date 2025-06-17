"""
增强的EPUB样式模块
Enhanced EPUB styles module
"""

class EnhancedStyles:
    """增强的样式类"""
    
    @staticmethod
    def get_main_css() -> str:
        """获取主要CSS样式"""
        return """
        /* 全局样式 - 优化阅读体验 */
        @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;700&display=swap');
        
        * {
            box-sizing: border-box;
        }
        
        body {
            font-family: "Noto Serif SC", "Source Han Serif SC", "Microsoft YaHei", "SimSun", serif;
            font-size: 16px;
            line-height: 1.8;
            margin: 0;
            padding: 2em 1.5em;
            color: #2c3e50;
            background-color: #fefefe;
            text-align: justify;
            word-wrap: break-word;
            hyphens: auto;
            -webkit-hyphens: auto;
            -moz-hyphens: auto;
            -ms-hyphens: auto;
        }
        
        /* 深色模式支持 */
        @media (prefers-color-scheme: dark) {
            body {
                background-color: #1a1a1a;
                color: #e0e0e0;
            }
            
            h1, h2 {
                color: #ffffff;
                border-color: #4a90e2;
            }
            
            .illustration img {
                border-color: #444;
                filter: brightness(0.9);
            }
        }
        
        /* 标题样式 - 更加优雅 */
        h1 {
            font-size: 1.8em;
            font-weight: 700;
            text-align: center;
            color: #34495e;
            margin: 1.5em 0 2em 0;
            padding: 1em 0;
            border-bottom: 3px solid #3498db;
            border-top: 1px solid #bdc3c7;
            background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 50%, #f8f9fa 100%);
            text-shadow: 0 1px 3px rgba(0,0,0,0.1);
            border-radius: 8px;
            position: relative;
            overflow: hidden;
        }
        
        h1::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
            animation: shimmer 3s infinite;
        }
        
        @keyframes shimmer {
            0% { left: -100%; }
            100% { left: 100%; }
        }
        
        h2 {
            font-size: 1.4em;
            font-weight: 500;
            color: #2c3e50;
            margin: 2em 0 1em 0;
            padding: 0.5em 0 0.5em 1em;
            border-left: 4px solid #3498db;
            background: linear-gradient(to right, #f8f9fa, transparent);
            border-radius: 0 8px 8px 0;
        }
        
        /* 段落样式 - 优化可读性 */
        p {
            text-indent: 2em;
            margin: 1.2em 0;
            line-height: 1.8;
            text-align: justify;
            word-spacing: 0.1em;
            letter-spacing: 0.02em;
        }
        
        /* 首段不缩进 */
        h1 + p, h2 + p, .chapter-separator + p {
            text-indent: 0;
            font-weight: 500;
        }
        
        /* 对话样式 - 更加生动 */
        p.dialogue {
            text-indent: 1em;
            margin-left: 1em;
            padding: 0.5em 1em;
            font-style: italic;
            color: #34495e;
            background: linear-gradient(to right, #ecf0f1, transparent);
            border-left: 3px solid #3498db;
            border-radius: 0 8px 8px 0;
            position: relative;
        }
        
        p.dialogue::before {
            content: '"';
            font-size: 1.5em;
            color: #3498db;
            position: absolute;
            left: -0.2em;
            top: -0.1em;
        }
        
        /* 强调文本 */
        em, i {
            font-style: italic;
            color: #e74c3c;
            font-weight: 500;
        }
        
        strong, b {
            font-weight: 700;
            color: #c0392b;
            text-shadow: 0 1px 1px rgba(0,0,0,0.1);
        }
        
        /* 图片样式 - 专业展示 */
        .illustration {
            text-align: center;
            margin: 3em 0;
            page-break-inside: avoid;
            background: #f8f9fa;
            padding: 2em;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        
        .illustration img {
            max-width: 100%;
            height: auto;
            border: 2px solid #ddd;
            border-radius: 12px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.15);
            transition: transform 0.3s ease;
        }
        
        .illustration img:hover {
            transform: scale(1.02);
        }
        
        .illustration-caption {
            font-size: 0.9em;
            color: #7f8c8d;
            margin-top: 1em;
            font-style: italic;
            font-weight: 500;
            padding: 0.5em 1em;
            background: rgba(255,255,255,0.8);
            border-radius: 20px;
            display: inline-block;
        }
        
        /* 分页控制 */
        .page-break {
            page-break-before: always;
        }
        
        /* 章节分隔 - 更加精美 */
        .chapter-separator {
            text-align: center;
            margin: 3em 0;
            font-size: 1.2em;
            color: #95a5a6;
            position: relative;
            padding: 1em 0;
        }
        
        .chapter-separator::before,
        .chapter-separator::after {
            content: '';
            position: absolute;
            top: 50%;
            width: 30%;
            height: 1px;
            background: linear-gradient(to right, transparent, #95a5a6, transparent);
        }
        
        .chapter-separator::before {
            left: 0;
        }
        
        .chapter-separator::after {
            right: 0;
        }
        
        /* 特殊文本样式 */
        .narrator {
            font-style: italic;
            color: #7f8c8d;
            text-align: center;
            margin: 2em 0;
            padding: 1em;
            background: linear-gradient(135deg, #f8f9fa, #ecf0f1);
            border-radius: 8px;
            border: 1px solid #bdc3c7;
        }
        
        .thought {
            font-style: italic;
            color: #8e44ad;
            background: linear-gradient(to right, rgba(142, 68, 173, 0.1), transparent);
            padding: 0.2em 0.5em;
            border-radius: 4px;
        }
        
        /* 响应式设计 */
        @media screen and (max-width: 600px) {
            body {
                padding: 1em 0.8em;
                font-size: 15px;
            }
            
            h1 {
                font-size: 1.6em;
                margin: 1em 0 1.5em 0;
            }
            
            h2 {
                font-size: 1.3em;
            }
            
            p {
                text-indent: 1.5em;
                line-height: 1.7;
            }
            
            .illustration {
                margin: 2em 0;
                padding: 1em;
            }
        }
        
        /* 打印样式 */
        @media print {
            body {
                font-size: 12pt;
                line-height: 1.6;
                color: black;
                background: white;
            }
            
            h1, h2 {
                color: black;
                page-break-after: avoid;
            }
            
            .illustration {
                page-break-inside: avoid;
                background: white;
                box-shadow: none;
            }
            
            .illustration img {
                max-width: 80%;
                box-shadow: none;
            }
        }
        
        /* 动画效果 */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        p, .illustration {
            animation: fadeIn 0.6s ease-out;
        }
        
        /* 选择文本样式 */
        ::selection {
            background: #3498db;
            color: white;
        }
        
        ::-moz-selection {
            background: #3498db;
            color: white;
        }
        """
    
    @staticmethod
    def get_navigation_css() -> str:
        """获取导航CSS样式"""
        return """
        /* 导航样式 */
        nav {
            font-family: "Noto Serif SC", "Microsoft YaHei", sans-serif;
            padding: 2em;
            background: linear-gradient(135deg, #f8f9fa, #ffffff);
            border-radius: 12px;
            margin: 2em 0;
        }
        
        nav h1 {
            color: #2c3e50;
            text-align: center;
            margin-bottom: 1.5em;
            font-size: 1.5em;
        }
        
        nav ol {
            list-style: none;
            margin: 0;
            padding: 0;
            counter-reset: chapter;
        }
        
        nav li {
            margin: 0.8em 0;
            counter-increment: chapter;
            position: relative;
        }
        
        nav li::before {
            content: counter(chapter, decimal-leading-zero);
            position: absolute;
            left: -2em;
            top: 0;
            color: #3498db;
            font-weight: bold;
            font-size: 0.9em;
        }
        
        nav a {
            text-decoration: none;
            color: #2c3e50;
            padding: 0.5em 1em;
            display: block;
            border-radius: 6px;
            transition: all 0.3s ease;
            border-left: 3px solid transparent;
        }
        
        nav a:hover {
            background: #3498db;
            color: white;
            border-left-color: #2980b9;
            transform: translateX(5px);
        }
        
        nav a:active {
            transform: translateX(2px);
        }
        """
