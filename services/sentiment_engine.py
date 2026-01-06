# 情感分析引擎
import joblib
import jieba
import os
from config import Config


class SentimentEngine:
    def __init__(self):
        self.model = None
        self.vectorizer = None
        self._load_model()

    def _load_model(self):
        """加载模型资源的内部方法"""
        if os.path.exists(Config.MODEL_PATH) and os.path.exists(Config.VEC_PATH):
            try:
                self.model = joblib.load(Config.MODEL_PATH)
                self.vectorizer = joblib.load(Config.VEC_PATH)
                print("✅ 情感分析引擎加载成功")
            except Exception as e:
                print(f"❌ 模型加载出错: {e}")
        else:
            print(f"❌ 未找到模型文件，请检查路径: {Config.MODEL_PATH}")

    def predict(self, text):
        """
        输入: 文本字符串
        输出: (标签, 置信度)
        """
        if not self.model or not text.strip():
            return "未知", 0.0

        # 分词 (保持和训练时一致)
        cut_text = " ".join(jieba.lcut(text))

        vec = self.vectorizer.transform([cut_text])
        probs = self.model.predict_proba(vec)[0]
        neg_prob, pos_prob = probs[0], probs[1]

        # 阈值判断
        if 0.45 <= pos_prob <= 0.55:
            return "😐 语气平淡/中性", pos_prob
        elif pos_prob > 0.55:
            return "😊 积极/友善", pos_prob
        else:
            return "😠 消极/冲突", neg_prob