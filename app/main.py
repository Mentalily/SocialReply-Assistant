import sys
from PyQt5.QtWidgets import QApplication
from ui_window import PopupWindow
from utils import predict_sentiment
from hotkey_listener import HotkeyListener

app = QApplication(sys.argv)
popup = PopupWindow() # 弹窗

listener = HotkeyListener()
'''
def on_hotkey():
    print("热键调用")
    text = pyperclip.paste()
    if text:
        label, score, reply = predict_sentiment(text)  # 调用模型
        popup.show_popup(text, label, score, reply)
'''
def handle_text(text):
    label, score, reply = predict_sentiment(text)
    popup.show_popup(text, label, score, reply)

listener.triggered.connect(handle_text)
listener.start()

# 注册全局快捷键 Ctrl+Shift+S
# keyboard.add_hotkey('ctrl+shift+c', on_hotkey)
print("程序已经启动")
sys.exit(app.exec_())
