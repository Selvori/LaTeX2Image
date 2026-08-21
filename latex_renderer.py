"""Pure LaTeX-to-PNG rendering logic used by LaTeX2Image."""

import io
import os
import re
import shutil
import subprocess
import tempfile

import fitz
from PIL import Image, ImageOps

from latex_config import (
    ANTIALIASING,
    CHINESE_FONT,
    DEFAULT_FONT_SIZE,
    ENABLE_CHINESE_SUPPORT,
    IMAGE_DPI,
    IMAGE_PADDING,
    MAX_FONT_SIZE,
    MIN_FONT_SIZE,
    PDF_MEDIA_BOX_PADDING,
    USE_MATH_FONTS,
    USE_STANDALONE_CLASS,
)


CJK_PATTERN = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")


def contains_chinese(text: str) -> bool:
    return CJK_PATTERN.search(text) is not None


def estimate_font_size(latex_code: str) -> int:
    """Estimate a display size from visible content rather than command names."""
    clean_text = re.sub(r"\\[a-zA-Z@]+", "", latex_code)
    clean_text = re.sub(r"\\.", "", clean_text)
    clean_text = re.sub(r"[\s{}_^$&#%~]", "", clean_text)
    length = len(clean_text)

    if length <= 5:
        return min(MAX_FONT_SIZE, DEFAULT_FONT_SIZE + 6)
    if length <= 10:
        return DEFAULT_FONT_SIZE
    if length <= 20:
        return max(MIN_FONT_SIZE, DEFAULT_FONT_SIZE - 2)
    return max(MIN_FONT_SIZE, DEFAULT_FONT_SIZE - 4)


def normalize_font_size(font_size: int) -> int:
    try:
        value = int(font_size)
    except (TypeError, ValueError) as exc:
        raise ValueError("font_size 必须是整数") from exc
    return max(MIN_FONT_SIZE, min(MAX_FONT_SIZE, value))


def build_latex_document(latex_code: str, font_size: int) -> str:
    """Build a document that applies arbitrary font sizes inside the body."""
    font_size = normalize_font_size(font_size)
    # Scaling the complete math box makes pdfTeX emit stable transformed
    # coordinates. Direct fractions can otherwise be mispositioned by MuPDF.
    scale_factor = f"{font_size / 10:.4f}".rstrip("0").rstrip(".")

    if USE_STANDALONE_CLASS:
        document_class = "standalone"
        document_options = ""
    else:
        document_class = "article"
        document_options = ""

    option_block = f"[{document_options}]" if document_options else ""
    header = rf"""\documentclass{option_block}{{{document_class}}}
\usepackage{{amsmath}}
\usepackage{{amssymb}}
\usepackage{{xcolor}}
\usepackage{{graphicx}}"""

    if USE_MATH_FONTS:
        header += r"""
\usepackage{bm}
\usepackage{lmodern}"""

    if ENABLE_CHINESE_SUPPORT and contains_chinese(latex_code):
        header += rf"""
\usepackage{{ctex}}
\setCJKmainfont{{{CHINESE_FONT}}}"""

    return rf"""{header}
\begin{{document}}
\scalebox{{{scale_factor}}}{{\(\displaystyle {latex_code}\)}}
\end{{document}}
"""


def compiler_for(latex_code: str) -> str:
    if ENABLE_CHINESE_SUPPORT and contains_chinese(latex_code):
        return "xelatex"
    return "pdflatex"


def _compile_pdf(tex_file: str, tmpdir: str, compiler: str) -> str:
    compiler_path = shutil.which(compiler)
    if not compiler_path:
        raise FileNotFoundError(f"未找到 {compiler}，请确认 TeX Live 或 MiKTeX 已加入 PATH")

    command = [
        compiler_path,
        "-interaction=nonstopmode",
        "-halt-on-error",
        "-no-shell-escape",
        "-output-directory",
        tmpdir,
        tex_file,
    ]

    print("正在编译 LaTeX……")
    try:
        subprocess.run(
            command,
            cwd=tmpdir,
            capture_output=True,
            check=True,
            timeout=60,
        )
    except subprocess.CalledProcessError as exc:
        output = (exc.stdout or b"") + b"\n" + (exc.stderr or b"")
        message = output.decode("utf-8", errors="replace").strip()
        raise RuntimeError(f"LaTeX 编译失败:\n{message}") from exc
    except subprocess.TimeoutExpired as exc:
        raise TimeoutError("LaTeX 编译超过 60 秒，请检查公式或降低 IMAGE_DPI") from exc

    pdf_file = os.path.join(tmpdir, "formula.pdf")
    if not os.path.exists(pdf_file):
        raise FileNotFoundError("LaTeX 编译完成，但未生成 formula.pdf")
    return pdf_file


def _render_pdf(pdf_file: str) -> Image.Image:
    antialiasing = max(0, min(int(ANTIALIASING), 8))
    fitz.graphics_antialias = antialiasing
    fitz.text_antialias = antialiasing

    with fitz.open(pdf_file) as pdf_document:
        page = pdf_document[0]
        media_box = page.mediabox
        pad = float(PDF_MEDIA_BOX_PADDING)
        page.set_mediabox(
            fitz.Rect(
                media_box.x0 - pad,
                media_box.y0 - pad,
                media_box.x1 + pad,
                media_box.y1 + pad,
            )
        )

        matrix = fitz.Matrix(IMAGE_DPI / 72, IMAGE_DPI / 72)
        pixmap = page.get_pixmap(matrix=matrix, alpha=False)
        rendered = Image.open(io.BytesIO(pixmap.tobytes("png"))).convert("RGB")
        rendered.load()

    content_box = ImageOps.invert(rendered.convert("L")).getbbox()
    if content_box:
        return rendered.crop(content_box)
    return rendered


def latex_to_image(latex_code: str, font_size: int | None = None) -> bytes:
    if not latex_code or not latex_code.strip():
        raise ValueError("LaTeX 公式不能为空")

    if font_size is None:
        font_size = estimate_font_size(latex_code)
    font_size = normalize_font_size(font_size)
    print(f"使用字体大小: {font_size}pt")

    with tempfile.TemporaryDirectory(prefix="latex2image-") as tmpdir:
        tex_file = os.path.join(tmpdir, "formula.tex")
        with open(tex_file, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(build_latex_document(latex_code, font_size))

        pdf_file = _compile_pdf(tex_file, tmpdir, compiler_for(latex_code))
        image = _render_pdf(pdf_file)

    output_image = Image.new(
        "RGB",
        (image.width + 2 * IMAGE_PADDING, image.height + 2 * IMAGE_PADDING),
        "white",
    )
    output_image.paste(image, (IMAGE_PADDING, IMAGE_PADDING))

    output = io.BytesIO()
    output_image.save(output, format="PNG", optimize=True)
    return output.getvalue()
