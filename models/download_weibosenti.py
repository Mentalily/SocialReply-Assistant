import pandas as pd

from datasets import load_dataset

print("正在从 dirtycomputer/weibo_senti_100k 下载...")

try:
    # 加载你找到的这个版本
    dataset = load_dataset("dirtycomputer/weibo_senti_100k")
    print("下载成功！")

    # 2. 转换为 DataFrame
    # 通常都在 'train' 分支里
    if 'train' in dataset:
        df = pd.DataFrame(dataset['train'])
    else:
        df = pd.DataFrame(dataset)

    # 3. 关键步骤：检查列名
    print(f"数据列名: {df.columns}")
    # 这一步是为了防止报错，看看文本列叫 'text' 还是 'review'

    # 如果列名叫 'text'，建议统一改成 'review'，方便后面代码不用改
    if 'text' in df.columns:
        df.rename(columns={'text': 'review'}, inplace=True)

    # 4. 简单的清洗：去重 & 去转发链
    print(f"原始数量: {len(df)}")
    df = df.dropna()
    # 去除转发内容 (// 之后的内容)
    df['review'] = df['review'].astype(str).apply(lambda x: x.split('//')[0])
    # 去除空文本
    df = df[df['review'].str.len() > 1]

    print(f"清洗后数量: {len(df)}")
    print(df.head())

    # 5. 保存
    save_path = "../data/weibo_senti_100k.csv"
    df.to_csv(save_path, index=False, encoding='utf-8')
    print(f"✅ 数据已准备好，保存至: {save_path}")

except Exception as e:
    print(f"❌ 出错了: {e}")
    print("建议检查网络，或者尝试方法二：直接下载 CSV 文件。")