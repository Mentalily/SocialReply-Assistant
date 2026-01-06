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

# x_train_vec是张巨大的表，行是样本句子，列是特征词，数据项是0-1的TF-IDF分数（特征词在样本句子中的重要程度）
# fit_transform基于训练数据产出规则（fit: 学习/你和），并根据规则转为数据
X_train_vec = vectorizer.fit_transform(X_train)
# transform使用刚才学习拟合的结果得到数字
X_test_vec = vectorizer.transform(X_test)

# C=1.0 正则化强度的倒数，C越大可能导致过拟合，C太小可能欠拟合
# liblinear 是专门为大规模稀疏数据（比如要处理的 20,000 维文本特征）设计的算法。在文本分类里，它通常跑得飞快且效果好。
# max_iter=1000 (最大迭代次数): 找最优权重的过程是慢慢磨出来的（梯度下降）
# 底层算法：z = (w1*x1)+(w2*x2)+...+bias. x1是特征值（TF-IDF计算结果），w1是权重，迭代多次不断修正得到的较优权重
# 再通过sigmoid函数映射到 0-1 区间
model = LogisticRegression(C=1.0, solver='liblinear', max_iter=1000)
# 根据答案不断修改权重以尽可能接近答案
model.fit(X_train_vec, y_train)

# ================== 3. 评估与保存 ==================
acc = accuracy_score(y_test, model.predict(X_test_vec))
print(f"训练完成！准确率: {acc:.4f}")

joblib.dump(model, '../data/sentiment_model.pkl')
joblib.dump(vectorizer, '../data/tfidf_vectorizer.pkl')
print("✅ 模型已保存")