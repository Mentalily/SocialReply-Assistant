import os
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

# 获取当前项目根目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Config:
    # 路径配置
    MODEL_PATH = os.path.join(BASE_DIR, 'data', 'sentiment_model.pkl')
    VEC_PATH = os.path.join(BASE_DIR, 'data', 'tfidf_vectorizer.pkl')

    # ✨ 新增：图标路径
    ICON_PATH = os.path.join(BASE_DIR, 'assets', 'chat.png')

    # API 配置
    API_KEY = os.getenv("SCHOOL_API_KEY", "empty")
    API_BASE_URL = os.getenv("SCHOOL_API_URL", "https://api.deepseek.com")
    MODEL_NAME = os.getenv("SCHOOL_MODEL_NAME", "deepseek-chat")