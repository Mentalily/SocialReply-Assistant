import pyperclip
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QTextEdit,
                             QPushButton, QHBoxLayout)
from PyQt5.QtCore import Qt, pyqtSignal, QThread, QObject
from PyQt5.QtGui import QFont


# --- 工作线程类 ---
class ReplyWorker(QThread):
    finished = pyqtSignal(str)

    def __init__(self, llm_engine, text, sentiment):
        super().__init__()
        self.llm_engine = llm_engine
        self.text = text
        self.sentiment = sentiment

    def run(self):
        # 调用业务层的逻辑
        result = self.llm_engine.generate_reply(self.text, self.sentiment)
        self.finished.emit(result)


# --- 主窗口类 ---
class MainWindow(QWidget):
    def __init__(self, sentiment_engine, llm_engine):
        super().__init__()
        # 依赖注入：窗口不负责创建引擎，而是由外部传入
        self.sentiment_engine = sentiment_engine
        self.llm_engine = llm_engine

        self.initUI()
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

    def initUI(self):
        self.setWindowTitle('社交语气分析助手')
        self.setGeometry(100, 100, 450, 500)  # 稍微高一点，放回复
        self.setStyleSheet("background-color: #f5f6f7;")  # 稍微灰一点的背景，护眼

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

        # 3. 回复生成区
        layout.addWidget(QLabel("💡 高情商回复参考:"))
        self.reply_area = QTextEdit()
        self.reply_area.setPlaceholderText("点击下方按钮，AI将为你生成三种回复策略...")
        self.reply_area.setStyleSheet("border: 1px solid #ddd; border-radius: 4px; padding: 5px; background: white;")
        layout.addWidget(self.reply_area)

        # 4. 按钮区
        btn_layout = QHBoxLayout()

        self.btn_api = QPushButton("✨ 生成高情商回复")
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
        """核心逻辑：被 Controller 或 Main 调用"""
        text = pyperclip.paste()
        if not text: return

        self.text_area.setText(text)
        self.btn_api.setEnabled(True)

        # 调用业务层
        label, score = self.sentiment_engine.predict(text)
        self.result_label.setText(f"{label} (置信度: {score:.2f})")
        self.showNormal()
        self.activateWindow()

    def start_api(self):
        text = self.text_area.toPlainText()
        sentiment = self.result_label.text()
        self.reply_area.setText("思考中...")
        self.btn_api.setEnabled(False)

        # 启动线程
        self.worker = ReplyWorker(self.llm_engine, text, sentiment)
        self.worker.finished.connect(lambda res: [self.reply_area.setText(res), self.btn_api.setEnabled(True)])
        self.worker.start()