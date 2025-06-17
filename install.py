"""
安装脚本
Installation script for the novel crawler
"""

import subprocess
import sys
import os

def run_command(command, description):
    """运行命令并显示结果"""
    print(f"\n{'='*50}")
    print(f"正在执行: {description}")
    print(f"命令: {command}")
    print('='*50)
    
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=True, text=True, encoding='utf-8')
        print("✅ 执行成功!")
        if result.stdout:
            print("输出:", result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print("❌ 执行失败!")
        print("错误:", e.stderr)
        return False
    except Exception as e:
        print("❌ 执行异常!")
        print("错误:", str(e))
        return False

def check_python_version():
    """检查Python版本"""
    print("检查Python版本...")
    version = sys.version_info
    print(f"当前Python版本: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python版本过低，需要Python 3.8或更高版本")
        return False
    
    print("✅ Python版本符合要求")
    return True

def install_requirements():
    """安装Python依赖包"""
    print("\n安装Python依赖包...")
    
    # 检查requirements.txt是否存在
    if not os.path.exists('requirements.txt'):
        print("❌ 找不到requirements.txt文件")
        return False
    
    # 升级pip
    print("升级pip...")
    run_command(f"{sys.executable} -m pip install --upgrade pip", "升级pip")
    
    # 安装依赖包
    return run_command(f"{sys.executable} -m pip install -r requirements.txt", 
                      "安装Python依赖包")

def install_playwright():
    """安装Playwright浏览器"""
    print("\n安装Playwright浏览器...")
    return run_command("playwright install chromium", "安装Chromium浏览器")

def create_directories():
    """创建必要的目录"""
    print("\n创建必要的目录...")
    
    directories = ['data', 'output', 'logs', 'data/images']
    
    for directory in directories:
        try:
            os.makedirs(directory, exist_ok=True)
            print(f"✅ 创建目录: {directory}")
        except Exception as e:
            print(f"❌ 创建目录失败 {directory}: {str(e)}")
            return False
    
    return True

def test_installation():
    """测试安装是否成功"""
    print("\n测试安装...")
    return run_command(f"{sys.executable} main.py --test", "测试网络连接")

def main():
    """主安装流程"""
    print("🚀 轻小说爬虫安装程序")
    print("=" * 50)
    
    # 检查Python版本
    if not check_python_version():
        sys.exit(1)
    
    # 安装Python依赖包
    if not install_requirements():
        print("❌ Python依赖包安装失败")
        sys.exit(1)
    
    # 安装Playwright浏览器
    if not install_playwright():
        print("❌ Playwright浏览器安装失败")
        print("💡 提示: 可以稍后手动运行 'playwright install chromium'")
    
    # 创建目录
    if not create_directories():
        print("❌ 目录创建失败")
        sys.exit(1)
    
    # 测试安装
    print("\n" + "="*50)
    print("🎉 安装完成!")
    print("="*50)
    
    print("\n📖 使用说明:")
    print("1. 爬取所有卷册: python main.py")
    print("2. 爬取指定卷册: python main.py --volumes \"第一卷\" \"第二卷\"")
    print("3. 测试连接: python main.py --test")
    print("4. 查看帮助: python main.py --help")
    
    print("\n📁 输出文件:")
    print("- EPUB文件: output/ 目录")
    print("- 日志文件: logs/ 目录")
    
    print("\n⚠️  注意事项:")
    print("- 请遵守网站使用条款和相关法律法规")
    print("- 仅供学习研究使用，请勿用于商业用途")
    print("- 建议在网站访问量较低的时间段运行")
    
    # 询问是否立即测试
    try:
        response = input("\n是否立即测试网络连接? (y/n): ").lower().strip()
        if response in ['y', 'yes', '是']:
            test_installation()
    except KeyboardInterrupt:
        print("\n安装完成，可以稍后手动测试。")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n安装被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n安装过程中出现异常: {str(e)}")
        sys.exit(1)
