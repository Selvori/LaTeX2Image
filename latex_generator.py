# latex_generator_fixed.py
import keyboard
import time
import pyperclip
import tempfile
import os
import subprocess
from PIL import Image
import win32clipboard
import io
import re

# 导入配置
from latex_config import (
    HOTKEY, SELECT_ALL_HOTKEY, CUT_HOTKEY, PASTE_HOTKEY,
    DEFAULT_FONT_SIZE, MIN_FONT_SIZE, MAX_FONT_SIZE,
    IMAGE_DPI, IMAGE_PADDING, USE_STANDALONE_CLASS,
    ENABLE_CHINESE_SUPPORT, CHINESE_FONT,
    ANTIALIASING, USE_MATH_FONTS
)

# 添加全局变量防止重复触发
is_processing = False

def copy_png_bytes_to_clipboard(png_bytes: bytes):
    """复制 PNG 图片到剪贴板"""
    image = Image.open(io.BytesIO(png_bytes))
    # 转换成 BMP 字节流（去掉 BMP 文件头的前 14 个字节）
    with io.BytesIO() as output:
        image.convert("RGB").save(output, "BMP")
        bmp_data = output.getvalue()[14:]

    # 打开剪贴板并写入 DIB 格式
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_DIB, bmp_data)
    win32clipboard.CloseClipboard()

def get_input_text() -> str:
    """
    获取输入框中的文本，使用更可靠的方法
    """
    # 备份原剪贴板
    old_clip = pyperclip.paste()
    
    # 方法1: 尝试使用复制操作
    pyperclip.copy("")
    time.sleep(0.1)
    
    # 发送复制命令
    keyboard.press('ctrl')
    keyboard.press('c')
    time.sleep(0.1)
    keyboard.release('c')
    keyboard.release('ctrl')
    time.sleep(0.3)  # 增加等待时间
    
    new_clip = pyperclip.paste()
    
    # 如果复制成功，返回内容
    if new_clip and new_clip != old_clip:
        pyperclip.copy(old_clip)
        return new_clip
    
    # 方法2: 如果复制失败，尝试全选+剪切
    print("复制失败，尝试剪切方式...")
    pyperclip.copy("")
    time.sleep(0.1)
    
    # 全选
    keyboard.press('ctrl')
    keyboard.press('a')
    time.sleep(0.1)
    keyboard.release('a')
    keyboard.release('ctrl')
    time.sleep(0.2)
    
    # 剪切
    keyboard.press('ctrl')
    keyboard.press('x')
    time.sleep(0.1)
    keyboard.release('x')
    keyboard.release('ctrl')
    time.sleep(0.3)  # 增加等待时间
    
    new_clip = pyperclip.paste()
    
    # 恢复原剪贴板
    pyperclip.copy(old_clip)
    
    return new_clip

def estimate_font_size(latex_code: str) -> int:
    """
    根据 LaTeX 代码长度估算合适的字体大小
    """
    # 移除 LaTeX 命令，只计算实际字符
    clean_text = re.sub(r'\\[a-zA-Z]+\{.*?\}', '', latex_code)
    clean_text = re.sub(r'\\[a-zA-Z]+', '', clean_text)
    clean_text = re.sub(r'[^a-zA-Z0-9\u4e00-\u9fff]', '', clean_text)  # 保留中文字符
    
    length = len(clean_text)
    
    # 根据长度调整字体大小
    if length <= 5:
        return min(MAX_FONT_SIZE, DEFAULT_FONT_SIZE + 6)
    elif length <= 10:
        return DEFAULT_FONT_SIZE
    elif length <= 20:
        return max(MIN_FONT_SIZE, DEFAULT_FONT_SIZE - 2)
    else:
        return max(MIN_FONT_SIZE, DEFAULT_FONT_SIZE - 4)

def contains_chinese(text):
    """检查文本是否包含中文字符"""
    return re.search(r'[\u4e00-\u9fff]', text) is not None

def latex_to_image(latex_code: str, font_size: int = None) -> bytes:
    """
    将 LaTeX 代码编译为图片
    """
    if font_size is None:
        font_size = estimate_font_size(latex_code)
    
    print(f"使用字体大小: {font_size}pt")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # 选择文档类
        if USE_STANDALONE_CLASS:
            document_class = "standalone"
            # 使用 varwidth 选项使宽度自适应
            document_options = f"preview,varwidth,{font_size}pt"
        else:
            document_class = "article"
            document_options = f"{font_size}pt"
        
        # 构建 LaTeX 头部
        latex_header = f"""\\documentclass[{document_options}]{{{document_class}}}
\\usepackage{{amsmath}}
\\usepackage{{amssymb}}
\\usepackage{{xcolor}}"""
        
        # 添加数学字体支持
        if USE_MATH_FONTS:
            latex_header += """
\\usepackage{bm}  % 粗体数学符号
\\usepackage{lmodern}  % 现代字体，更清晰"""
            print("使用高质量数学字体")
        
        # 添加中文支持（如果启用且文本包含中文）
        if ENABLE_CHINESE_SUPPORT and contains_chinese(latex_code):
            latex_header += f"""
\\usepackage{{ctex}}
\\setCJKmainfont{{{CHINESE_FONT}}}"""
            print("启用中文支持")
        
        # LaTeX 内容
        latex_content = f"""{latex_header}
\\begin{{document}}
\\[ {latex_code} \\]
\\end{{document}}"""
        
        tex_file = os.path.join(tmpdir, "formula.tex")
        with open(tex_file, "w", encoding="utf-8") as f:
            f.write(latex_content)
        
        try:
            # 编译 LaTeX 到 PDF
            # 对于中文，可能需要使用 xelatex 而不是 pdflatex
            compiler = "pdflatex"
            if ENABLE_CHINESE_SUPPORT and contains_chinese(latex_code):
                compiler = "xelatex"  # xelatex 对中文支持更好
            
            # 添加高质量输出选项
            if compiler == "pdflatex":
                extra_options = "-draftmode -interaction=nonstopmode"
            else:
                extra_options = "-no-pdf -interaction=nonstopmode"
            
            # 第一次编译
            result = subprocess.run(
                f'{compiler} {extra_options} -output-directory "{tmpdir}" "{tex_file}"',
                capture_output=True, shell=True, check=True
            )
            
            # 第二次编译（确保引用正确）
            result = subprocess.run(
                f'{compiler} -interaction=nonstopmode -output-directory "{tmpdir}" "{tex_file}"',
                capture_output=True, shell=True, check=True
            )
            
            # 转换 PDF 为 PNG
            pdf_file = os.path.join(tmpdir, "formula.pdf")
            
            # 使用 PyMuPDF 转换
            import fitz
            pdf_document = fitz.open(pdf_file)
            page = pdf_document[0]
            
            # 获取页面边界框
            rect = page.rect
            zoom = IMAGE_DPI / 72  # 72是PDF的标准DPI
            
            # 创建高质量pixmap
            matrix = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=matrix, alpha=False)
            img_data = pix.tobytes("png")
            pdf_document.close()
            
            # 使用PIL处理图片，添加边距
            image = Image.open(io.BytesIO(img_data))
            
            # 创建带边距的新图片
            new_width = image.width + 2 * IMAGE_PADDING
            new_height = image.height + 2 * IMAGE_PADDING
            new_image = Image.new("RGB", (new_width, new_height), "white")
            new_image.paste(image, (IMAGE_PADDING, IMAGE_PADDING))
            
            # 转换为字节
            output = io.BytesIO()
            new_image.save(output, format="PNG", optimize=True)
            
            return output.getvalue()
            
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.decode('utf-8', errors='ignore') if e.stderr else str(e)
            raise Exception(f"LaTeX 编译失败: {error_msg}")

def safe_paste():
    """安全地执行粘贴操作"""
    # 确保所有按键都已释放
    keyboard.release('ctrl')
    keyboard.release('v')
    time.sleep(0.1)
    
    # 执行粘贴
    keyboard.press('ctrl')
    time.sleep(0.05)
    keyboard.press('v')
    time.sleep(0.05)
    keyboard.release('v')
    time.sleep(0.05)
    keyboard.release('ctrl')

def Start():
    """主函数"""
    global is_processing
    
    # 防止重复触发
    if is_processing:
        print("正在处理中，请稍候...")
        return
        
    is_processing = True
    
    try:
        print("开始生成 LaTeX 公式图片...")

        # 获取输入框中的文本
        text = get_input_text()
        if not text or text.strip() == "":
            print("输入框为空或无法获取文本")
            print("请确保:")
            print("1. 光标在输入框中")
            print("2. 输入框中有文本内容")
            print("3. 程序有足够的权限访问剪贴板")
            return
        
        print(f"获取到的文本: {text}")

        try:
            # 生成图片
            png_bytes = latex_to_image(text)
            
            # 复制到剪贴板
            copy_png_bytes_to_clipboard(png_bytes)
            print("✓ 公式图片已生成并复制到剪贴板")
            
            # 等待一小段时间确保剪贴板已更新
            time.sleep(0.3)
            
            # 安全地粘贴
            safe_paste()
            print("✓ 已粘贴公式图片")
            
        except Exception as e:
            print(f"生成失败: {e}")
            # 如果失败，尝试恢复原始文本
            try:
                pyperclip.copy(text)
                safe_paste()
                print("已恢复原始文本")
            except:
                print("无法恢复原始文本")
    finally:
        # 重置处理状态
        is_processing = False

# 绑定热键 - 使用 suppress=False 避免干扰其他按键
keyboard.add_hotkey(HOTKEY, Start, suppress=False)

print("LaTeX 公式生成器已启动")
print(f"热键: {HOTKEY}")
print(f"默认字体大小: {DEFAULT_FONT_SIZE}pt")
print(f"图片分辨率: {IMAGE_DPI} DPI")
print(f"抗锯齿级别: {ANTIALIASING}")
print(f"中文支持: {'启用' if ENABLE_CHINESE_SUPPORT else '禁用'}")
print("使用方法:")
print("1. 在任意输入框中输入 LaTeX 公式")
print("2. 确保光标在该输入框中")
print("3. 按热键生成公式图片")
print("4. 公式图片会自动替换输入框中的文本")
print("=" * 50)
print("如果遇到'输入框为空'的问题，请尝试:")
print("1. 确保输入框中有文本")
print("2. 以管理员身份运行此程序")
print("3. 检查是否有其他程序占用剪贴板")

# 保持程序运行
try:
    keyboard.wait()
except KeyboardInterrupt:
    print("程序退出")