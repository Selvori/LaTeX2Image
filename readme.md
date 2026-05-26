# LaTeX 公式图片生成器

一键将 LaTeX 数学公式转换为高清图片，并自动粘贴到微信、QQ、编辑器等任意输入框。

## 功能特点

- **实时转换** — 输入 LaTeX 公式，一键生成图片并自动粘贴
- **自适应大小** — 根据公式长度自动调整字号和图片尺寸
- **中文支持** — 公式中可混合使用中文与数学符号
- **高度可配置** — 自定义热键、字体、DPI、抗锯齿等
- **即贴即用** — 生成后自动粘贴，无需手动操作

## 运行效果

```
输入: \int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}
按 Ctrl+Shift+L
等待 2-5 秒 → 公式被替换为高清图片
```

---

## 环境要求

- **操作系统**：Windows
- **Python**：3.6 或更高版本
- **LaTeX 发行版**：TeX Live（推荐）或 MiKTeX（需包含 `pdflatex` 和 `xelatex`）

---

## 安装步骤

### 1. 安装 Python

下载并安装 Python：https://www.python.org/downloads/

**注意**：安装时务必勾选 **"Add Python to PATH"**。

### 2. 安装 LaTeX 环境

推荐使用 **TeX Live**：

1. 下载 ISO：[https://mirrors.tuna.tsinghua.edu.cn/CTAN/systems/texlive/Images/](https://mirrors.tuna.tsinghua.edu.cn/CTAN/systems/texlive/Images/)
2. 解压后以管理员身份运行 `install-tl-windows.bat`
3. 安装完成后确保 `pdflatex` 和 `xelatex` 在系统 PATH 中（打开 cmd，输入 `pdflatex --version` 验证）

### 3. 安装 Python 依赖

打开终端（Win+R → `cmd`），运行：

```cmd
pip install -r requirements.txt
```

或逐一手动安装：

```cmd
pip install keyboard pyperclip pillow pymupdf pywin32
```

### 4. 下载程序

将以下两个文件放在**同一文件夹**（新建一个文件夹存放）：

- [`latex_generator.py`](latex_generator.py) — 主程序
- [`latex_config.py`](latex_config.py) — 配置文件

---

## 使用方法

1. **启动程序**：双击 `latex_generator.py`，或在终端运行：

   ```cmd
   python latex_generator.py
   ```

   启动后控制台会显示配置信息和操作提示。

2. **输入公式**：在任意输入框（微信、QQ、浏览器、编辑器等）中输入 LaTeX 公式（**不需要** `$$` 包裹），例如：

   ```
   \int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}
   ```

3. **生成图片**：确保光标仍在输入框中，按 **`Ctrl+Shift+L`**（默认热键）。

4. **自动粘贴**：等待 2-5 秒后，原文本将自动替换为公式图片。

### 停止程序

在运行程序的终端窗口中按 **`Ctrl+C`** 即可退出。

---

## 配置文件说明

编辑 [`latex_config.py`](latex_config.py) 可自定义所有行为：

```python
# ===== 热键配置 =====
HOTKEY = "ctrl+shift+l"      # 触发生成的热键

# ===== 字体配置 =====
DEFAULT_FONT_SIZE = 12       # 默认字号（pt）
MIN_FONT_SIZE = 8            # 最小字号
MAX_FONT_SIZE = 72           # 最大字号

# ===== LaTeX 编译配置 =====
IMAGE_DPI = 600              # 图片分辨率（越高越清晰，生成越慢）
IMAGE_PADDING = 20           # 图片边距（像素）
ENABLE_CHINESE_SUPPORT = True   # 是否启用中文支持
CHINESE_FONT = "SimSun"      # 中文字体（如 "Microsoft YaHei"）
COMPILE_TIMES = 1            # 编译次数（公式 1 次足够；含交叉引用时需 2 次）

# ===== 图片质量 =====
ANTIALIASING = 16            # 抗锯齿 (1-16，越高越清晰)
USE_MATH_FONTS = True        # 使用高质量数学字体
```

### 常用调整参考

| 目标 | 调整方式 |
|------|----------|
| 加快生成速度 | 降低 `IMAGE_DPI`（如 300）、降低 `ANTIALIASING`（如 4） |
| 提高图片清晰度 | 提高 `IMAGE_DPI`（如 1200）、提高 `ANTIALIASING`（如 16） |
| 更换触发热键 | 修改 `HOTKEY`（如 `"f1"`、`"alt+q"`） |
| 公式过小/过大 | 调整 `DEFAULT_FONT_SIZE` |

---

## 常见问题

### 程序显示"输入框为空"或无法获取文本

1. 确保输入框中**有文本内容**
2. 确保**光标在输入框中**且在**最上层窗口**
3. 以**管理员身份**运行程序（右键 cmd → 以管理员身份运行，再执行 `python latex_generator.py`）
4. 检查是否有其他程序占用剪贴板

### 图片模糊

- 增加 `IMAGE_DPI`（如 1200、2400）
- 增加 `ANTIALIASING`（如 8、16）

### 生成速度慢

- 降低 `IMAGE_DPI`（如 300、200）
- 降低 `ANTIALIASING`（如 4、2）
- 保持 `COMPILE_TIMES = 1`（公式无需两次编译）

### 中文显示为方块或乱码

- 确保系统中安装了指定的中文字体（`SimSun` 是宋体）
- 尝试修改 `CHINESE_FONT` 为其他字体名称，如 `"Microsoft YaHei"`（微软雅黑）、`"SimHei"`（黑体）、`"KaiTi"`（楷体）
- 如果使用 MiKTeX，可能需要额外安装 `ctex` 宏包

### 热键冲突（按热键没反应）

- 修改 `HOTKEY` 配置为其他组合键，如 `"ctrl+alt+l"`、`"f1"`
- 关闭可能冲突的其他快捷键工具（如截图工具、输入法快捷键）

### 提示"pdflatex 未找到"或 LaTeX 编译失败

- 确认 TeX Live 已安装且 `pdflatex` 在 PATH 中。打开终端验证：
  ```cmd
  pdflatex --version
  ```
- 如果系统是 64 位，TeX Live 可能安装在 `C:\texlive\2024\bin\windows\`，需将此路径添加到系统 PATH

### 程序运行时出现 __pycache__ 文件夹

这是 Python 自动生成的缓存目录，可安全忽略或删除。再次运行时会重新生成。

---

## 技术说明

- **PDF→PNG 转换**：使用 PyMuPDF（`fitz`）进行高质量渲染，支持任意 DPI
- **临时文件清理**：生成的 `.tex`、`.pdf`、`.aux`、`.log` 文件位于系统临时目录，退出后自动删除
- **文档类**：默认使用 `standalone` + `varwidth`，自动适配公式宽度
- **剪贴板**：使用 `pywin32` 直接写入 DIB 格式，兼容各类 IM 输入框

## 文件说明

| 文件 | 作用 |
|------|------|
| `latex_generator.py` | 主程序，包含热键监听、LaTeX 编译、图片生成、自动粘贴 |
| `latex_config.py` | 用户配置文件，所有可调参数在此修改 |
| `requirements.txt` | Python 依赖列表，`pip install -r requirements.txt` 安装 |

---

## 声明

本项目由 AI 辅助完成。
