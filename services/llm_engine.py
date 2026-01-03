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
        我是一个不善言辞的人，对方发来：“{input_text}”
        我的分析程序判断语气为：【{sentiment}】。
        
        请生成 3 条回复建议（分别对应：1.得体礼貌 2.热情高情商 3.机智防御）。
        
        ⚠️ 格式严格要求：
        1. 不要输出任何开场白、序号或结束语。
        2. 仅输出3条具体回复内容。
        3. 3条内容之间使用 "|||" 符号分隔。
        
        例如：
        好的，明白了|||哇，这都被你发现了|||也就是那样吧
        """

        try:
            response = self.client.chat.completions.create(
                model=Config.MODEL_NAME,
                messages=[
                    {"role": "system", "content": "你是一个严格遵守格式指令的辅助程序。"},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7
            )
            raw_text = response.choices[0].message.content.strip()

            # 💡 解析逻辑：把长字符串切分成列表
            # 如果 AI 没听话，没用 ||| 分隔，我们就按换行符强行切
            if "|||" in raw_text:
                replies = raw_text.split("|||")
            else:
                replies = raw_text.split("\n")

            # 清理一下每条回复的前后空格，并过滤空行
            clean_replies = [r.strip() for r in replies if r.strip()]

            # 确保只有3条，多余的不要，少了补空
            return clean_replies[:3]

        except Exception as e:
            return f"API 调用失败: {str(e)}"