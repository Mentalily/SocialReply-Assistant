import os
import sys
import joblib
import keyboard
import pyperclip
import jieba
from dotenv import load_dotenv
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel,
                             QTextEdit, QPushButton, QHBoxLayout, QMessageBox)
from PyQt5.QtCore import Qt, pyqtSignal, QObject, QThread
from PyQt5.QtGui import QFont
from openai import OpenAI  # 导入 OpenAI 库

# ================= 配置区域 (请修改这里!) =================
MODEL_PATH = '../data/sentiment_model.pkl'
VEC_PATH = '../data/tfidf_vectorizer.pkl'

load_dotenv()

# 使用ECNU大模型
API_KEY = os.getenv("SCHOOL_API_KEY")
BASE_URL = os.getenv("SCHOOL_API_URL")
MODEL_NAME = os.getenv("SCHOOL_MODEL_NAME")


# ========================================================

class SentimentAnalyzer:
    def __init__(self):
        try:
            self.model = joblib.load(MODEL_PATH)
            self.vectorizer = joblib.load(VEC_PATH)
            # 加载停用词表(如果训练时用了的话)，这里假设你没用或者逻辑很简单
        except Exception as e:
            print(f"❌ 模型加载失败: {e}")
            self.model = None

    def predict(self, text):
        if not self.model: return "模型未加载", 0.0

        # 保持和训练时一致的分词逻辑
        # 如果你训练时没去停用词，这里就这样写：
        cut_text = " ".join(jieba.lcut(text))

        vec = self.vectorizer.transform([cut_text])
        probs = self.model.predict_proba(vec)[0]

        # 这里的逻辑和之前一样
        neg_prob, pos_prob = probs[0], probs[1]

        if 0.45 <= pos_prob <= 0.55:
            return "😐 语气平淡/中性", pos_prob
        elif pos_prob > 0.55:
            return "😊 积极/友善", pos_prob
        else:
            return "😠 消极/冲突", neg_prob


# ================= 核心升级：API 工作线程 =================
# 为什么要用 QThread？因为网络请求会卡住主界面。
# 用了线程，点击按钮后界面不会“未响应”，体验极佳。
class ReplyGenerator(QThread):
    finished_signal = pyqtSignal(str)  # 信号：任务完成传回文本

    def __init__(self, input_text, sentiment):
        super().__init__()
        self.input_text = input_text
        self.sentiment = sentiment

    def run(self):
        try:
            client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

            # 精心设计的 Prompt (提示词工程)
            # 专门针对“不善社交”的场景设计
            prompt = f"""
            我是一个不善言辞的人，现在对方发来一句话：
            “{self.input_text}”

            我的情感分析程序判断这句话的语气是：【{self.sentiment}】。

            请做我的“高情商嘴替”，帮我生成 3 条不同风格的回复建议：
            1. 🤝 【得体/礼貌】：适合普通社交或工作，结束话题或客气回应。
            2. 🔥 【热情/高情商】：适合朋友或想拉近关系，接住梗或提供情绪价值。
            3. 🛡️ 【机智/防御】：如果对方语气不善，帮我软钉子回击；如果对方是熟人，帮我幽默互怼。

            请直接给出回复内容，不要过多的解释。
            """

            response = client.chat.completions.create(
                model=MODEL_NAME,  # 或者 "moonshot-v1-8k"
                messages=[
                    {"role": "system", "content": "你是一个精通人情世故的高情商社交助手。"},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,  # 稍微有点创意
                stream=False
            )

            result = response.choices[0].message.content
            self.finished_signal.emit(result)

        except Exception as e:
            self.finished_signal.emit(f"API 调用出错: {str(e)}\n请检查网络或 API Key。")


# ================= 键盘监听线程 =================
class HotkeyHandler(QObject):
    trigger_signal = pyqtSignal()


class MainWindow(QWidget):
    def __init__(self, analyzer):
        super().__init__()
        self.analyzer = analyzer
        self.initUI()
        self.setWindowFlags(Qt.WindowStaysOnTopHint)  # 置顶

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
        self.btn_api.clicked.connect(self.start_api_generation)
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

    def update_analysis(self):
        """监听到剪贴板后的回调"""
        text = pyperclip.paste()
        if not text or len(text.strip()) == 0: return

        self.text_area.setText(text)
        self.reply_area.clear()  # 清空旧回复
        self.btn_api.setEnabled(True)  # 重置按钮状态
        self.btn_api.setText("✨ 生成高情商回复")

        # 本地模型秒出结果
        label, score = self.analyzer.predict(text)

        self.result_label.setText(f"{label} (置信度: {score:.2f})")

        # 动态变色
        if "积极" in label:
            style = "color: #155724; background-color: #d4edda; border: 1px solid #c3e6cb;"
        elif "消极" in label:
            style = "color: #721c24; background-color: #f8d7da; border: 1px solid #f5c6cb;"
        else:
            style = "color: #383d41; background-color: #e2e3e5; border: 1px solid #d6d8db;"
        self.result_label.setStyleSheet(style + "border-radius: 4px; padding: 10px;")

        self.showNormal()
        self.activateWindow()

    def start_api_generation(self):
        """开始调用 API"""
        input_text = self.text_area.toPlainText()
        sentiment = self.result_label.text()

        if not input_text: return

        self.reply_area.setText("🔄 正在思考中，请稍候...")
        self.btn_api.setEnabled(False)  # 防止重复点击
        self.btn_api.setText("生成中...")

        # 启动线程
        self.worker = ReplyGenerator(input_text, sentiment)
        self.worker.finished_signal.connect(self.on_api_finished)
        self.worker.start()

    def on_api_finished(self, result_text):
        """API 返回后的回调"""
        self.reply_area.setText(result_text)
        self.btn_api.setEnabled(True)
        self.btn_api.setText("✨ 重新生成")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    analyzer = SentimentAnalyzer()
    window = MainWindow(analyzer)

    handler = HotkeyHandler()
    handler.trigger_signal.connect(window.update_analysis)


    def on_hotkey():
        handler.trigger_signal.emit()


    try:
        # 注册热键
        keyboard.add_hotkey('ctrl+shift+c', on_hotkey, suppress=False)
        print("🚀 社交助手已启动！选中文字按 Ctrl+Shift+C 即可。")
    except Exception as e:
        print(f"热键注册失败: {e}")

    sys.exit(app.exec_())