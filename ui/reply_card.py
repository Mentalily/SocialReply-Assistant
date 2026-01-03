import pyperclip
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor


class ReplyCard(QFrame):
    def __init__(self, text):
        super().__init__()
        self.text_content = text
        self.initUI()

    def initUI(self):
        # 卡片样式：白底，圆角，浅边框
        self.setStyleSheet("""
            ReplyCard {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 6px;
                margin-bottom: 5px;
            }
            ReplyCard:hover {
                border: 1px solid #0078d7; /* 鼠标悬停变蓝 */
            }
        """)

        layout = QHBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)  # 内边距

        # 1. 回复内容 (自动换行)
        self.lbl_text = QLabel(self.text_content)
        self.lbl_text.setWordWrap(True)  # 允许长文本换行
        self.lbl_text.setStyleSheet("border: none; color: #333; font-size: 13px;")
        layout.addWidget(self.lbl_text, stretch=1)  # stretch=1 表示占满剩余空间

        # 2. 复制按钮
        self.btn_copy = QPushButton("复制")
        self.btn_copy.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_copy.setFixedSize(50, 25)
        self.btn_copy.clicked.connect(self.copy_text)
        self.btn_copy.setStyleSheet("""
            QPushButton {
                background-color: #f0f0f0;
                border: none;
                border-radius: 4px;
                color: #555;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
                color: #000;
            }
        """)
        layout.addWidget(self.btn_copy)

        self.setLayout(layout)

    def copy_text(self):
        """复制逻辑 + 视觉反馈"""
        pyperclip.copy(self.text_content)

        # 让按钮文字变一下，提示用户成功了
        self.btn_copy.setText("已复制")
        self.btn_copy.setStyleSheet("background-color: #d4edda; color: #155724;")  # 变绿

        # 1秒后变回去 (可选，需要QTimer，这里简单处理就不变回去了，或者下次打开重置)