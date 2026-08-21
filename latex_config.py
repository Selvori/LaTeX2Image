"""LaTeX2Image 用户配置文件。

修改配置后需要重启程序才能生效。字符串内容请保留引号。
"""

# ==================== 快捷键 ====================

# 生成公式图片的全局快捷键。
# 写法示例："ctrl+shift+l"、"ctrl+alt+q"、"f8"。
HOTKEY = "ctrl+shift+l"

# 程序读取和替换输入框内容时使用的系统快捷键。
# Windows 用户通常不需要修改下面三项。
SELECT_ALL_HOTKEY = "ctrl+a"
COPY_HOTKEY = "ctrl+c"
PASTE_HOTKEY = "ctrl+v"


# ==================== 公式大小 ====================

# 默认字号，单位为 pt。数值越大，生成的公式图片越大。
DEFAULT_FONT_SIZE = 12

# 自动调整字号时允许使用的最小值和最大值，单位为 pt。
# 长公式会趋向 MIN_FONT_SIZE，短公式会趋向较大的字号。
MIN_FONT_SIZE = 8
MAX_FONT_SIZE = 72


# ==================== 图片质量 ====================

# 图片分辨率，单位为 DPI。
# 300 生成较快；600 更清晰；继续提高会明显增加内存占用和处理时间。
IMAGE_DPI = 600

# 公式四周保留的白色边距，单位为像素。
IMAGE_PADDING = 20

# 抗锯齿等级，有效范围为 0～8。
# 数值越大边缘通常越平滑，推荐保持 8。
ANTIALIASING = 8


# ==================== LaTeX 编译 ====================

# 使用 standalone 文档类自动适配公式页面大小。
# 推荐保持 True；改为 False 可能生成很大的空白页面。
USE_STANDALONE_CLASS = True

# 是否在检测到中文时启用中文编译支持。
# 启用后，含中文的公式会使用 xelatex 和 ctex。
ENABLE_CHINESE_SUPPORT = True

# 中文字体名称，必须是 Windows 中已经安装的字体。
# 常用值："SimSun"（宋体）、"Microsoft YaHei"（微软雅黑）、"SimHei"（黑体）。
CHINESE_FONT = "SimSun"

# 是否加载 bm 和 lmodern，以获得更完整、清晰的数学字体支持。
USE_MATH_FONTS = True


# ==================== 页面裁切 ====================

# 渲染前向四周扩展 PDF 页面边界，单位为 pt。
# 用于防止分式、根号和上下标贴近页面边缘时被裁掉。
# 默认 30 通常足够；只有仍发生裁切时才需要提高。
PDF_MEDIA_BOX_PADDING = 30
