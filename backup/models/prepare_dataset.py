import pandas as pd
import re
from snownlp import SnowNLP
from sklearn.model_selection import train_test_split

# ================== 1. 读取数据 ==================
data_path = "../../data/12万对话语料青云库.csv"

inputs = []
replies = []

with open(data_path, "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        line = line.strip()
        if "|" not in line:
            continue
        # 只按第一个 | 分割
        parts = line.split("|", 1)
        if len(parts) == 2:
            inputs.append(parts[0].strip())
            replies.append(parts[1].strip())

df = pd.DataFrame({
    "input": inputs,
    "reply": replies
})

print(f"成功读取数据条数: {len(df)}")
print(df.head())


# ================== 2. 文本清洗函数 ==================
def clean_text(text: str) -> str:
    """基础文本清洗：去占位符 / 不可见字符 / 压缩连续标点"""
    if not isinstance(text, str):
        return ""

    # 去首尾空白
    text = text.strip()

    # 去 {xxx} 这类占位符
    text = re.sub(r'\{.*?\}', '', text)

    # 去不可见字符
    text = re.sub(r'[\u200b-\u200f\u202a-\u202e]', '', text)

    # 连续标点压缩
    text = re.sub(r'[!?！？]{2,}', '！', text)
    text = re.sub(r'[。.]{2,}', '。', text)

    return text


# ================== 3. 数据清洗 ==================
df = df[['input', 'reply']]  # 保留必要字段
df = df.dropna().astype(str)  # 去空 & 转字符串
df['input'] = df['input'].apply(clean_text)
df['reply'] = df['reply'].apply(clean_text)
# 去除清洗后过短样本
df = df[(df['input'].str.len() >= 2) & (df['reply'].str.len() >= 2)]
df = df.reset_index(drop=True)
print(f"清洗后数据条数: {len(df)}")


# ================== 4. 粗粒度脏词 / 敏感内容标注 ==================
bad_words = ["骚货", "勾引", "巴操", "尿", "性"]  # 可扩展

def check_offensive(text: str) -> bool:
    return any(w in text for w in bad_words)

def coarse_label(row):
    """粗粒度标签：
       - 不良内容 -> '不良'
       - 正常文本 -> 积极 / 中性 / 消极
    """
    if check_offensive(row['input']) or check_offensive(row['reply']):
        return '不良'
    try:
        s = SnowNLP(row['input'])
        score = s.sentiments
    except:
        score = 0.5

    if score >= 0.6:
        return '积极'
    elif score <= 0.4:
        return '消极'
    else:
        return '中性'

df['coarse_label'] = df.apply(coarse_label, axis=1)


# ================== 5. 精细情感打分 ==================
def sentiment_label(text: str):
    """返回 (label, score)"""
    if not isinstance(text, str) or len(text.strip()) == 0:
        return "中性", 0.5
    try:
        s = SnowNLP(text)
        score = s.sentiments
    except:
        return "中性", 0.5

    if score >= 0.6:
        label = "积极"
    elif score <= 0.4:
        label = "消极"
    else:
        label = "中性"
    return label, score

labels_scores = df['input'].apply(sentiment_label)
df['label'] = labels_scores.apply(lambda x: x[0])
df['score'] = labels_scores.apply(lambda x: x[1])

print(df.head(10))


# ================== 6. 拆分训练集和测试集 ==================
train_df, test_df = train_test_split(df, test_size=0.1, random_state=42, shuffle=True)
train_df.to_csv("../data/train_dataset.csv", index=False)
test_df.to_csv("../data/test_dataset.csv", index=False)

print(f"训练集: {len(train_df)}, 测试集: {len(test_df)}")
print("数据处理完成 ✅")
