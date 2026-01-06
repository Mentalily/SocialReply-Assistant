import pandas as pd
import re
import jieba
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# ================== 1. 读取与清洗数据 ==================
print("正在读取微博数据...")
df = pd.read_csv("../data/weibo_senti_100k.csv")
df['review'] = df['review'].astype(str)


def clean_and_cut(text):
    # 1. 正则清洗 (去URL, 去@)
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    text = re.sub(r'@[\w\u4e00-\u9fa5]+', '', text)
    text = re.sub(r'回复@.*?:', '', text)

    # 2. 分词
    words = jieba.lcut(text)

    return " ".join(words)


print("正在处理文本...")
df['cut_review'] = df['review'].apply(clean_and_cut)

# 去除处理后变为空的行
df = df[df['cut_review'].str.len() > 0]

# ================== 2. 训练模型 ==================
X = df['cut_review']
y = df['label']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

# TF-IDF 特征提取 (Feature Extraction)
# 这里就是把汉字转换成数字矩阵的过程
# max_features=5000 表示只保留最重要的5000个词，防止数据量太大
vectorizer = TfidfVectorizer(max_features=20000, ngram_range=(1, 2)) # 同时提取 1-gram (单个词) 和 2-gram (双词组合) 作为特征

X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

model = LogisticRegression(C=1.0, solver='liblinear', max_iter=1000)
model.fit(X_train_vec, y_train)

# ================== 3. 评估与保存 ==================
acc = accuracy_score(y_test, model.predict(X_test_vec))
print(f"训练完成！准确率: {acc:.4f}")

joblib.dump(model, '../data/sentiment_model.pkl')
joblib.dump(vectorizer, '../data/tfidf_vectorizer.pkl')
print("✅ 模型已保存")