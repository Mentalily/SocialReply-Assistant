import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("SCHOOL_API_KEY")
base_url = os.getenv("SCHOOL_API_URL")
model_name = os.getenv("SCHOOL_MODEL_NAME")

# 检查是否读取成功
if not api_key:
    raise ValueError("❌ 错误：未找到 API_KEY，请检查 .env 文件！")

# 替换成学校的信息
client = OpenAI(
    base_url=base_url,
    api_key=api_key,
)

try:
    response = client.chat.completions.create(
        model="ecnu-max", # 记得问管理员这个名字叫什么
        messages=[
            {"role": "user", "content": "你好，测试一下连接。"}
        ]
    )
    print("✅ 连接成功！回复是：", response.choices[0].message.content)
except Exception as e:
    print("❌ 连接失败:", e)