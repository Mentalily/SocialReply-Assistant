import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app')))
import json
import codecs
import csv
# from utils import predict_sentiment_api  # 你可以把调用API的函数放在 utils.py

# 路径
DIALOG_JSON = "../data/NaturalConv_Release_20210318/dialog_release.json"
OUTPUT_CSV = "../data/naturalconv_labeled.csv"


def load_dialogs(json_path):
    """读取 NaturalConv 的对话数据"""
    with codecs.open(json_path, "r", "utf-8") as f:
        dialog_list = json.load(f)
    return dialog_list


def process_dialogs(dialog_list, max_rounds=5):
    """
    将对话拆分成单轮文本，并打情感标签
    max_rounds: 每条对话最多保留几轮
    """
    processed_data = []
    for dialog in dialog_list:
        content = dialog.get("content", [])
        # content 是一轮轮的列表，每轮可能是 dict 或 list
        for round_text in content[:max_rounds]:
            # 假设每轮是 {"speaker": "A", "utterance": "..."}
            if isinstance(round_text, dict):
                text = round_text.get("utterance", "").strip()
            else:
                text = str(round_text).strip()
            if not text:
                continue

            # 调用情感分析 API 打标签
            label, score, reply_example = predict_sentiment_api(text)

            # 保存到列表
            processed_data.append({
                "text": text,
                "label": label,
                "score": score,
                "reply": reply_example
            })
    return processed_data


def save_to_csv(data, csv_path):
    """保存到 CSV 文件"""
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["text", "label", "score", "reply"])
        writer.writeheader()
        for row in data:
            writer.writerow(row)


if __name__ == "__main__":
    dialogs = load_dialogs(DIALOG_JSON)
    print(f"共加载 {len(dialogs)} 条对话")
    processed = process_dialogs(dialogs, max_rounds=5)
    print(f"处理后得到 {len(processed)} 条单轮数据")
    save_to_csv(processed, OUTPUT_CSV)
    print(f"已保存到 {OUTPUT_CSV}")
