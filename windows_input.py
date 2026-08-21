"""Windows keyboard, focus, and clipboard operations for LaTeX2Image."""

import io
import time

import keyboard
import pyperclip
from PIL import Image
import win32clipboard
import win32gui

from latex_config import COPY_HOTKEY, PASTE_HOTKEY, SELECT_ALL_HOTKEY


class InputStateChangedError(RuntimeError):
    """Raised when focus or text changes while a formula is rendering."""


def release_modifier_keys() -> None:
    for key in ("ctrl", "shift", "alt"):
        keyboard.release(key)
    time.sleep(0.05)


def send_hotkey(hotkey_str: str, hold: float = 0.15, after: float = 0.3) -> None:
    keys = hotkey_str.split("+")
    for key in keys:
        keyboard.press(key)
        time.sleep(0.02)
    time.sleep(hold)
    for key in reversed(keys):
        keyboard.release(key)
        time.sleep(0.02)
    time.sleep(after)


def _clipboard_text() -> str:
    value = pyperclip.paste()
    return value if isinstance(value, str) else str(value)


def _open_clipboard(timeout: float = 1.0) -> None:
    deadline = time.monotonic() + timeout
    while True:
        try:
            win32clipboard.OpenClipboard()
            return
        except Exception:
            if time.monotonic() >= deadline:
                raise
            time.sleep(0.05)


def _capture_clipboard() -> list[tuple[int, str | bytes]]:
    """Capture clipboard formats that pywin32 can safely copy and restore."""
    snapshot = []
    _open_clipboard()
    try:
        format_id = 0
        while True:
            format_id = win32clipboard.EnumClipboardFormats(format_id)
            if not format_id:
                break
            try:
                data = win32clipboard.GetClipboardData(format_id)
            except Exception:
                continue
            if isinstance(data, str):
                snapshot.append((format_id, data))
            elif isinstance(data, (bytes, bytearray, memoryview)):
                snapshot.append((format_id, bytes(data)))
    finally:
        win32clipboard.CloseClipboard()
    return snapshot


def _restore_clipboard(snapshot: list[tuple[int, str | bytes]]) -> None:
    _open_clipboard()
    try:
        win32clipboard.EmptyClipboard()
        for format_id, data in snapshot:
            try:
                win32clipboard.SetClipboardData(format_id, data)
            except Exception:
                # Some owner-defined formats cannot be reconstructed after capture.
                continue
    finally:
        win32clipboard.CloseClipboard()


def read_current_input_text(timeout: float = 1.5, keep_selection: bool = False) -> str:
    """Select and copy the focused input without removing its contents."""
    release_modifier_keys()
    clipboard_snapshot = _capture_clipboard()
    sentinel = f"__LATEX2IMAGE_PENDING_{time.time_ns()}__"

    copied_text = None
    try:
        pyperclip.copy(sentinel)
        send_hotkey(SELECT_ALL_HOTKEY, after=0.15)
        send_hotkey(COPY_HOTKEY, after=0.05)

        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            current_text = _clipboard_text()
            if current_text != sentinel:
                copied_text = current_text
                break
            time.sleep(0.05)
        if copied_text is None:
            raise RuntimeError("复制输入内容超时，请确认焦点位于可编辑文本框中")
    finally:
        _restore_clipboard(clipboard_snapshot)

    if not keep_selection:
        # Collapse the temporary select-all so the source text is not left selected
        # throughout the potentially slow TeX compilation.
        send_hotkey("right", hold=0.02, after=0.05)
    return copied_text


def copy_png_bytes_to_clipboard(png_bytes: bytes) -> None:
    image = Image.open(io.BytesIO(png_bytes))
    with io.BytesIO() as output:
        image.convert("RGB").save(output, "BMP")
        dib_data = output.getvalue()[14:]

    _open_clipboard()
    try:
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, dib_data)
    finally:
        win32clipboard.CloseClipboard()


def get_foreground_window() -> int:
    return int(win32gui.GetForegroundWindow())


def replace_current_input_with_image(
    source_window: int,
    expected_text: str,
    png_bytes: bytes,
) -> None:
    """Replace only when focus and the selected input text are unchanged."""
    if get_foreground_window() != source_window:
        raise InputStateChangedError("处理期间活动窗口发生变化")

    current_text = read_current_input_text(keep_selection=True)
    if current_text != expected_text:
        raise InputStateChangedError("处理期间输入内容发生变化")

    copy_png_bytes_to_clipboard(png_bytes)
    release_modifier_keys()
    send_hotkey(PASTE_HOTKEY, hold=0.05, after=0.1)
