import pandas as pd
import re
import jieba
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# ================== 1. 准备停用词 ==================
'''
stopwords_path = "../data/hit_stopwords.txt"  # 假设你下载并保存了这个文件

def load_stopwords(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            # 读取所有行，去空格，转为集合(set)查找更快
            return set([line.strip() for line in f])
    except FileNotFoundError:
        print("⚠️ 警告：没找到停用词文件，将不使用停用词。")
        return set()


stop_words = load_stopwords(stopwords_path)
print(f"已加载 {len(stop_words)} 个停用词")
'''

# ================== 2. 读取与清洗数据 ==================
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

    # 3. 去停用词 & 去除短词/空格
    # 这里的逻辑是：如果词不在停用词表里，且不是纯空格，就保留
    #filtered_words = [w for w in words if w not in stop_words and len(w.strip()) > 0]

    #return " ".join(filtered_words)
    return " ".join(words)


print("正在处理文本...")
df['cut_review'] = df['review'].apply(clean_and_cut)

# 去除处理后变为空的行
df = df[df['cut_review'].str.len() > 0]

# ================== 3. 训练模型 ==================
X = df['cut_review']
y = df['label']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

# token_pattern=r"(?u)\b\w+\b" 是默认值，它会自动忽略标点和表情
# 我们已经在 clean_and_cut 里处理好了，这里直接用
vectorizer = TfidfVectorizer(max_features=20000, ngram_range=(1, 2))

X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

model = LogisticRegression(C=1.0, solver='liblinear', max_iter=1000)
model.fit(X_train_vec, y_train)

# ================== 4. 评估与保存 ==================
acc = accuracy_score(y_test, model.predict(X_test_vec))
print(f"训练完成！准确率: {acc:.4f}")

joblib.dump(model, '../data/sentiment_model.pkl')
joblib.dump(vectorizer, '../data/tfidf_vectorizer.pkl')
print("✅ 模型已保存")