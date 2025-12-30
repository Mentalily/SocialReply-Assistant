from PyQt5.QtCore import QThread, pyqtSignal
import keyboard
import pyperclip


class HotkeyListener(QThread):
    triggered = pyqtSignal(str)

    def run(self):
        keyboard.add_hotkey('ctrl+shift+c', self.on_hotkey)
        keyboard.wait()  # 阻塞在子线程，不影响 UI

    def on_hotkey(self):
        text = pyperclip.paste()
        if text:
            self.triggered.emit(text)
