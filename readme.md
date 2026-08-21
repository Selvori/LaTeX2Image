# LaTeX 公式图片生成器

一个面向 Windows 的工具。它可以读取当前输入框中的 LaTeX 公式，将公式编译为 PNG 图片，并自动替换原文本。

## 主要功能

- 使用 `Ctrl+Shift+L` 全局热键生成公式图片
- 根据公式内容自动调整显示大小
- 使用 PyMuPDF 按指定 DPI 渲染 PDF

## 运行环境

- Python 3.10+
- TeX Live 或 MiKTeX
- `pdflatex` 和 `xelatex` 位于环境变量
- 中文公式需要 `ctex` 宏包和可用的中文字体

## 安装

### 1. 安装 Python 依赖

```powershell
python -m pip install -r requirements.txt
```

如果系统找不到 `python` 命令，可以改用 Windows Python Launcher：

```powershell
py -m pip install -r requirements.txt
```

### 2. 检查 LaTeX 环境

```powershell
pdflatex --version
xelatex --version
```

## 启动

```powershell
python latex_generator.py
```

如果系统找不到 `python` 命令：

```powershell
py latex_generator.py
```

启动成功后，终端会显示当前热键、DPI、字号和中文支持状态。

### 使用虚拟环境

不是必要条件。

```powershell
python -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe latex_generator.py
```

## 使用方法

1. 在支持文本输入和图片粘贴的窗口中输入 LaTeX 公式。
2. 不要使用 `$$...$$` 包裹公式，只输入公式正文。
3. 保持输入框焦点，按 `Ctrl+Shift+L`。
4. 等待程序完成编译和图片渲染。
5. 如果窗口和文本均未变化，原公式会被图片替换。若窗口发生了变化，生成的图片会位于剪贴板。

示例：

```latex
\int_{-\infty}^{\infty} e^{-x^2}\,dx = \sqrt{\pi}
```

中文建议放在 `\text{}` 中，例如：

```latex
E = mc^2 \quad \text{质能方程}
```

## 配置

可自行修改 `latex_config.py`。
