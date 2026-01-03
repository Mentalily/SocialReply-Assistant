import pyperclip
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QTextEdit,
                             QPushButton, QHBoxLayout, QScrollArea)
from PyQt5.QtCore import Qt, pyqtSignal, QThread, QObject
from PyQt5.QtGui import QFont, QCursor, QIcon
from ui.reply_card import ReplyCard
from config import Config


# --- 工作线程类 ---
class ReplyWorker(QThread):
    finished = pyqtSignal(list)  # 信号携带列表数据

    def __init__(self, llm_engine, text, sentiment):
        super().__init__()
        self.llm_engine = llm_engine
        self.text = text
        self.sentiment = sentiment

    def run(self):
        # 调用业务层的逻辑，获取回复列表
        result_list = self.llm_engine.generate_reply(self.text, self.sentiment)
        self.finished.emit(result_list)


# --- 主窗口类 ---
class MainWindow(QWidget):
    def __init__(self, sentiment_engine, llm_engine):
        super().__init__()
        self.sentiment_engine = sentiment_engine
        self.llm_engine = llm_engine

        self.initUI()
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

    def initUI(self):
        self.setWindowTitle('SocialReply-Assistant')
        self.setGeometry(100, 100, 550, 550)
        self.setWindowIcon(QIcon(Config.ICON_PATH))
        self.setStyleSheet("background-color: #f5f6f7;")

        layout = QVBoxLayout()

        # 1. 原文区
        layout.addWidget(QLabel("对方发来的话:"))
        self.text_area = QTextEdit()
        self.text_area.setMaximumHeight(60)
        self.text_area.setStyleSheet("border: 1px solid #ddd; border-radius: 4px; padding: 5px; background: white;")
        self.text_area.setReadOnly(True)
        layout.addWidget(self.text_area)

        # 2. 情感分析结果区
        self.result_label = QLabel("等待划词...")
        self.result_label.setFont(QFont("Microsoft YaHei", 12, QFont.Bold))
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("background: #e9ecef; border-radius: 4px; padding: 10px;")
        layout.addWidget(self.result_label)

        # 3. 回复生成区 (ScrollArea 容器)
        layout.addWidget(QLabel("💡 建议回复 (点击复制):"))

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("border: none; background-color: transparent;")

        self.scroll_content = QWidget()
        self.replies_layout = QVBoxLayout(self.scroll_content)
        self.replies_layout.setContentsMargins(0, 0, 0, 0)
        self.replies_layout.addStretch()  # 弹簧

        self.scroll_area.setWidget(self.scroll_content)
        layout.addWidget(self.scroll_area)

        # 4. 按钮区
        btn_layout = QHBoxLayout()

        self.btn_api = QPushButton("✨ 生成回复")
        self.btn_api.clicked.connect(self.start_api)
        self.btn_api.setStyleSheet("""
            QPushButton { background-color: #007bff; color: white; border-radius: 5px; padding: 8px; font-weight: bold; }
            QPushButton:hover { background-color: #0056b3; }
            QPushButton:disabled { background-color: #a0a0a0; }
        """)

        self.btn_close = QPushButton("关闭")
        self.btn_close.clicked.connect(self.hide)
        self.btn_close.setStyleSheet("padding: 8px;")

        btn_layout.addWidget(self.btn_api)
        btn_layout.addWidget(self.btn_close)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def handle_clipboard(self):
        self.clear_replies()
        self.btn_api.setText("✨ 生成回复")

        text = pyperclip.paste()
        if not text: return

        self.text_area.setText(text)
        self.btn_api.setEnabled(True)

        label, score = self.sentiment_engine.predict(text)
        self.result_label.setText(f"{label} (置信度: {score:.2f})")

        # 移动鼠标位置
        cursor_pos = QCursor.pos()
        self.move(cursor_pos.x() + 20, cursor_pos.y() + 20)

        self.showNormal()
        self.activateWindow()

    def start_api(self):
        """修复后的 API 调用逻辑"""
        text = self.text_area.toPlainText()
        sentiment = self.result_label.text()

        self.btn_api.setText("生成中...")  # 修复点
        self.btn_api.setEnabled(False)
        self.clear_replies()

        self.worker = ReplyWorker(self.llm_engine, text, sentiment)
        # 修复点：连接到正确的槽函数，而不是 lambda
        self.worker.finished.connect(self.on_api_finished)
        self.worker.start()

    def on_api_finished(self, replies_list):
        """API 返回后，动态生成卡片"""
        self.btn_api.setEnabled(True)
        self.btn_api.setText("✨ 重新生成")

        for reply_text in replies_list:
            card = ReplyCard(reply_text)
            # 在倒数第1个位置插入 (即弹簧之前)
            count = self.replies_layout.count()
            if count > 0:
                self.replies_layout.insertWidget(count - 1, card)
            else:
                self.replies_layout.addWidget(card)

    def clear_replies(self):
        """清空界面上的卡片"""
        while self.replies_layout.count() > 1:  # 保留最后一个 Stretch
            item = self.replies_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()