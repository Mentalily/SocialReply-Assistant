import os
import json
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

# 获取当前项目根目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Config:
    # 路径配置
    MODEL_PATH = os.path.join(BASE_DIR, 'data', 'sentiment_model.pkl')
    VEC_PATH = os.path.join(BASE_DIR, 'data', 'tfidf_vectorizer.pkl')

    # ✨ 美化部分
    ICON_PATH = os.path.join(BASE_DIR, 'assets', 'chat.png')     # logo
    THEME_PATH = os.path.join(BASE_DIR, 'assets', 'theme.json')  # 主题路径

    # API 配置
    API_KEY = os.getenv("SCHOOL_API_KEY", "empty")
    API_BASE_URL = os.getenv("SCHOOL_API_URL", "https://api.deepseek.com")
    MODEL_NAME = os.getenv("SCHOOL_MODEL_NAME", "deepseek-chat")

    # ✨ 新增：加载主题的方法
    @staticmethod
    def load_theme():
        try:
            with open(Config.THEME_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️ 加载主题失败，使用默认配色: {e}")
            # 返回一套默认的，防止程序崩溃
            return {
                "app_bg": "#F0F0F0", "primary": "#0078D7",
                "card_bg": "#FFFFFF", "text_main": "#333"
            }

# 程序启动时直接加载，作为一个静态变量供全局使用
THEME = Config.load_theme()