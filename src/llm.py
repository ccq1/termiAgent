import os 

from openai import OpenAI
from typing import Generator
# 开发环境引入
from dotenv import load_dotenv


load_dotenv()  # 加载 .env 文件




class LLM:
    def __init__(self):
        self.client = self.create_client()
        self.model = "deepseek-chat"
        self.temperature = 0.7
        self.max_tokens = 1000

    def create_client(self):
        return OpenAI(api_key=os.getenv("OPENAI_API_KEY"),base_url=os.getenv("OPENAI_BASE_URL"))

    def chat_llm(self, prompt: str) -> Generator:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}],
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            stream=True,
        )

        # for chunk in response:
        #     if chunk.choices[0].finish_reason == "stop":
        #         yield chunk.choices[0].text
        #     else:
        #         yield chunk.choices[0].text

        return response




if __name__ == "__main__":
    llm = LLM()
    response = llm.chat_llm("Hello, world!")
    for chunk in response:
        print(chunk)

    
    