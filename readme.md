**LaTeX 公式图片生成器**

一个可以将 LaTeX 数学公式实时转换为图片并自动粘贴到输入框的 Windows 工具。

~~和朋友线上交流数学题的时候终于不需要用大脑编译对方发来的LaTeX公式啦(确信~~

**功能特点**

实时转换：输入 LaTeX 公式，一键生成图片

自适应大小：根据公式内容自动调整图片尺寸

中文支持：完美支持中文字符和数学符号

高度可配置：可自定义热键、字体大小、图片质量等

多平台支持：支持微信、QQ等输入框(理论上只要支持图片输入那就行)

**环境要求**

Windows 操作系统

Python 3.6 或更高版本

**安装步骤**

1. 安装 Python 环境
   
下载并安装 Python：https://www.python.org/downloads/

注意：安装时务必勾选 "Add Python to PATH"

2. 安装 LaTeX 环境
   
推荐使用 TeX Live，下载地址：

https://mirrors.tuna.tsinghua.edu.cn/CTAN/systems/texlive/Images/

下载 texlive.iso 文件，解压后运行 install-tl-windows.bat 进行安装。

3. 安装 Python 依赖库
   
打开cmd(按下win+r，输入cmd并回车)，运行以下命令：

pip install keyboard pyperclip pillow pymupdf pywin32

4. 下载程序文件

下载本项目中的两个文件到同一文件夹：

latex_generator.py（主程序）

latex_config.py（配置文件）

**使用方法**

运行程序

在任意输入框（微信、QQ等）中输入 LaTeX 公式(不需要$$)

确保该页面在最上层

按 Ctrl+Shift+L（默认热键）

等待 2-5 秒，公式图片会自动替换输入框中的文本


**自定义配置**

编辑 latex_config.py 文件来自定义程序行为：

```#修改热键

HOTKEY = "ctrl+shift+l"  # 改为 "f1", "alt+l" 等

#调整字体大小

DEFAULT_FONT_SIZE = 12   # 默认字体大小

MIN_FONT_SIZE = 8        # 最小字体大小  

MAX_FONT_SIZE = 72       # 最大字体大小

#调整图片质量

IMAGE_DPI = 300          # 图片分辨率（越高越清晰，但生成越慢）

ANTIALIASING = 2         # 抗锯齿级别（1-16）

#中文支持

ENABLE_CHINESE_SUPPORT = True    # 启用中文支持

CHINESE_FONT = "SimSun"          # 中文字体
```

**常见问题**

1. 程序显示"输入框为空"
   
确保输入框中有文本内容

以管理员身份运行程序

检查是否有其他程序占用剪贴板

运行后同目录下会出现__pycache__文件夹，删不删无所谓，再运行还会出来的


2. 图片模糊
   
增加 IMAGE_DPI 值（如 600/1200/2400...）

增加 ANTIALIASING 值（如 4/8/16）

3. 生成速度慢
   
降低 IMAGE_DPI 值（如 200）

降低 ANTIALIASING 值（如 1）

设置 COMPILE_TIMES = 1

4. 中文显示异常
   
确保系统中安装了指定的中文字体

尝试修改 CHINESE_FONT 为其他字体名称

5. 热键冲突
   
修改 HOTKEY 配置为其他组合键

关闭可能冲突的其他快捷键工具

**技术说明**

程序使用 PyMuPDF 进行高质量的 PDF 到 PNG 转换

生成的临时文件会自动删除，不会占用磁盘空间

支持 standalone 文档类，自动调整图片大小适应公式内容


**文件说明**

latex_generator.py - 主程序文件

latex_config.py - 配置文件


**AI声明**

本程序90%以上的内容由AI生成



