'''
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
import pyperclip
import pyautogui


class PopupWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setStyleSheet("background-color: #f0f0f0; border: 1px solid #333;")
        self.resize(500, 300)
        self.label = QLabel("", self)
        self.label.setFont(QFont("Helvetica", 12))
        self.label.move(10, 10)
        self.button = QPushButton("复制回复", self)
        self.button.move(80, 80)
        self.button.clicked.connect(self.copy_reply)
        self.reply_text = ""

        # 自动隐藏
        self.timer = QTimer()
        self.timer.timeout.connect(self.hide)
        self.timer.setSingleShot(True)

    def show_popup(self, text, label, score, reply):
        self.reply_text = reply
        self.label.setText(f"文本: {text[:20]}...\n情感: {label} ({score:.2f})\n示例回复: {reply}")
        x, y = pyautogui.position()  # 弹窗显示在鼠标旁
        self.move(x + 10, y + 10)
        self.show()
        self.raise_()
        self.timer.start(5000)  # 5秒后自动隐藏

    def copy_reply(self):
        pyperclip.copy(self.reply_text)
'''

from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QFrame
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
import pyperclip
import pyautogui


class PopupWindow(QWidget):
    def __init__(self):
        super().__init__()

        # 无边框 + 置顶
        self.setWindowFlags(
            Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool
        )

        # 关键：防止黑屏
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        self.resize(360, 200)

        # ===== 内容容器 =====
        self.container = QFrame(self)
        self.container.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border-radius: 12px;
                border: 1px solid #cccccc;
            }
        """)
        self.container.setGeometry(0, 0, 360, 200)

        layout = QVBoxLayout(self.container)
        layout.setContentsMargins(15, 15, 15, 15)

        self.label = QLabel("")
        self.label.setWordWrap(True)
        self.label.setFont(QFont("Microsoft YaHei", 10))
        layout.addWidget(self.label)

        self.button = QPushButton("复制示例回复")
        self.button.setCursor(Qt.PointingHandCursor)
        self.button.clicked.connect(self.copy_reply)
        layout.addWidget(self.button)

        self.reply_text = ""

        # 自动隐藏
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.hide)

    def show_popup(self, text, label, score, reply):
        self.reply_text = reply
        self.label.setText(
            f"📌 原文：{text[:40]}...\n\n"
            f"😊 情感：{label}（{score:.2f}）\n\n"
            f"💬 示例回复：\n{reply}"
        )

        x, y = pyautogui.position()
        self.move(x + 15, y + 15)

        self.show()
        self.raise_()
        self.activateWindow()

        self.timer.start(6000)

    def copy_reply(self):
        pyperclip.copy(self.reply_text)


