"""Global-hotkey entry point for LaTeX2Image."""

import threading

import keyboard

from latex_config import (
    ANTIALIASING,
    DEFAULT_FONT_SIZE,
    ENABLE_CHINESE_SUPPORT,
    HOTKEY,
    IMAGE_DPI,
)
from latex_renderer import latex_to_image
from windows_input import (
    InputStateChangedError,
    copy_png_bytes_to_clipboard,
    get_foreground_window,
    read_current_input_text,
    replace_current_input_with_image,
)


processing_lock = threading.Lock()


def process_current_input() -> bool:
    """Render the focused input's text and replace it without deleting it first."""
    if not processing_lock.acquire(blocking=False):
        print("正在处理中，请稍候……")
        return False

    try:
        source_window = get_foreground_window()
        text = read_current_input_text()
        if not text or not text.strip():
            print("输入框为空或无法读取文本。")
            return False

        print(f"读取到文本: {text}")
        png_bytes = latex_to_image(text)

        try:
            replace_current_input_with_image(source_window, text, png_bytes)
            print("公式图片已生成并粘贴。")
            return True
        except InputStateChangedError as exc:
            copy_png_bytes_to_clipboard(png_bytes)
            print(f"未自动替换：{exc}")
            print("原文本未被删除，图片已复制到剪贴板，可手动粘贴。")
            return False
        except Exception as exc:
            copy_png_bytes_to_clipboard(png_bytes)
            print(f"自动粘贴失败：{exc}")
            print("原文本通常仍在输入框中，图片已复制到剪贴板。")
            return False
    except Exception as exc:
        print(f"生成失败：{exc}")
        print("转换前未删除原文本。")
        return False
    finally:
        processing_lock.release()


def print_startup_help() -> None:
    print("LaTeX 公式图片生成器已启动")
    print(f"热键: {HOTKEY}")
    print(f"默认字体大小: {DEFAULT_FONT_SIZE}pt")
    print(f"图片分辨率: {IMAGE_DPI} DPI")
    print(f"抗锯齿级别: {ANTIALIASING}")
    print(f"中文支持: {'启用' if ENABLE_CHINESE_SUPPORT else '禁用'}")
    print("使用方法:")
    print("1. 在当前输入框中输入 LaTeX 公式")
    print("2. 保持输入框焦点并按下热键")
    print("3. 处理期间不要切换窗口或修改输入内容")
    print("=" * 50)


def main() -> None:
    keyboard.add_hotkey(HOTKEY, process_current_input, suppress=False)
    print_startup_help()
    try:
        keyboard.wait()
    except KeyboardInterrupt:
        print("程序退出")
    finally:
        keyboard.unhook_all_hotkeys()


if __name__ == "__main__":
    main()
