import pyperclip
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QCursor
from config import THEME


class ReplyCard(QFrame):
    def __init__(self, text):
        super().__init__()
        self.text_content = text
        self.initUI()

    def initUI(self):
        # 卡片样式：白底，圆角，浅边框
        self.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border: 1px solid #EEF2F6;
                border-radius: 8px;
                /* 稍微给点底部边框模拟立体感 */
                border-bottom: 2px solid #E2E8F0; 
            }
            QFrame:hover {
                background-color: #F8FAFC;
                border: 1px solid #EF8257; /* 悬停变蓝框 */
                border-bottom: 2px solid #3B82F6;
            }
            QLabel {
                border: none;
                background: transparent;
                color: #252422;
                font-size: 13px;
                line-height: 1.4; /* 增加行高，阅读更舒服 */
            }
        """)

        layout = QHBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)  # 内边距

        # 1. 回复内容 (自动换行)
        self.lbl_text = QLabel(self.text_content)
        self.lbl_text.setWordWrap(True)  # 允许长文本换行
        self.lbl_text.setStyleSheet("border: none; color: #54798C; font-size: 23px;")
        layout.addWidget(self.lbl_text, stretch=1)  # stretch=1 表示占满剩余空间

        # 2. 复制按钮
        self.btn_copy = QPushButton("Copy")
        self.btn_copy.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_copy.setFixedSize(50, 25)
        self.btn_copy.clicked.connect(self.copy_text)

        self.default_btn_style = f"""
            QPushButton {{
                background-color: #f0f0f0;
                border: none;
                border-radius: 4px;
                color: #555;
                font-size: 12px;
                font-weight: bold;
                padding: 2px;
            }}
            QPushButton:hover {{
                background-color: #e0e0e0;
                color: {THEME["text_sub"]};
            }}
        """

        self.btn_copy.setStyleSheet(self.default_btn_style)

        layout.addWidget(self.btn_copy)
        self.setLayout(layout)

    def copy_text(self):
        """复制逻辑 + 视觉反馈"""
        pyperclip.copy(self.text_content)

        # 让按钮文字变一下，提示用户成功了
        self.btn_copy.setText("Done")
        self.btn_copy.setStyleSheet(f"""
            QPushButton {{
                background-color: {THEME['success']};
                color: {THEME['text_sub']};
                border-radius: 4px;
                font-size: 12px;
                font-weight: bold;
                padding: 2px;
            }}
        """)  # 变绿

        # 1秒后变回去 (可选，需要QTimer，这里简单处理就不变回去了，或者下次打开重置)
        QTimer.singleShot(400, self.reset_button)

    def reset_button(self):
        """恢复原来的样子"""
        # 恢复文字
        self.btn_copy.setText("Copy")
        # 恢复样式 (使用我们在 initUI 里定义的变量)
        self.btn_copy.setStyleSheet(self.default_btn_style)