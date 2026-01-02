# 大模型引擎
from openai import OpenAI
from config import Config


class LLMEngine:
    def __init__(self):
        self.client = OpenAI(
            api_key=Config.API_KEY,
            base_url=Config.API_BASE_URL
        )

    def generate_reply(self, input_text, sentiment):
        """
        发送请求给大模型并返回文本
        """
        prompt = f"""
        我是一个不善言辞的人，现在对方发来一句话：
        “{input_text}”
        我的情感分析程序判断这句话的语气是：【{sentiment}】。

        请做我的“高情商嘴替”，帮我生成 3 条不同风格的回复建议：
        1. 🤝 【得体/礼貌】
        2. 🔥 【热情/高情商】
        3. 🛡️ 【机智/防御】
        """

        try:
            response = self.client.chat.completions.create(
                model=Config.MODEL_NAME,
                messages=[
                    {"role": "system", "content": "你是一个高情商社交助手。"},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"API 调用失败: {str(e)}"