# latex_config.py
# LaTeX 公式生成器配置

# ===== 热键配置 =====
# 生成公式的热键
HOTKEY = "ctrl+shift+l"

# 全选热键
SELECT_ALL_HOTKEY = "ctrl+a"

# 剪切热键
CUT_HOTKEY = "ctrl+x"

# 粘贴热键
PASTE_HOTKEY = "ctrl+v"

# ===== 字体和大小配置 =====
# 默认字体大小（pt）
DEFAULT_FONT_SIZE = 12

# 最小字体大小
MIN_FONT_SIZE = 8

# 最大字体大小
MAX_FONT_SIZE = 72

# ===== LaTeX 编译配置 =====
# 图片分辨率（DPI）- 提高这个值可以增加清晰度
IMAGE_DPI = 4800  # 从 300 提高到 600

# 图片边距（像素）
IMAGE_PADDING = 20

# 是否使用 standalone 文档类（推荐，可以自动调整页面大小）
USE_STANDALONE_CLASS = True

# 是否启用中文支持
ENABLE_CHINESE_SUPPORT = True

# 中文字体（需要系统中已安装）
CHINESE_FONT = "SimSun"  # 宋体，也可以改为 "Microsoft YaHei" 等

# ===== 图片质量配置 =====
# 抗锯齿级别 (1-16，越高越清晰但处理时间越长)
ANTIALIASING = 16

# 是否使用高质量数学字体
USE_MATH_FONTS = True