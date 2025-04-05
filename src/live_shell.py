import os
import subprocess
import sys
import time
from typing import List, Generator
from rich.live import Live
from rich.panel import Panel
from rich.markdown import Markdown
import openai

# 配置 OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY", "your-api-key-here")
openai.api_base = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")

class InteractiveShell:
    PANELS = {"assistant": {"title": "AI Assistant", "border_style": "blue"}}
    console = sys.stdout

    def __init__(self):
        self.shell = os.getenv("SHELL", "/bin/bash")
        self.history: List[str] = []
        self.process = None

    def start_shell(self):
        """启动交互式 shell"""
        # 使用 -i 强制交互模式，确保 shell 接受命令
        self.process = subprocess.Popen(
            [self.shell, "-i"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            env=os.environ.copy()  # 继承环境变量
        )
        print(f"启动交互式 shell: {self.shell}")
        self.run()

    def run(self):
        try:
            while True:
                user_input = input(">>> ").strip()
                if user_input.lower() == "exit":
                    break
                elif user_input.startswith("AI:"):
                    self.call_ai(user_input[3:].strip())
                else:
                    self.execute_command(user_input)
        except KeyboardInterrupt:
            print("\n退出交互式 shell")
        finally:
            if self.process:
                self.process.terminate()

    def execute_command(self, command: str):
        """执行 shell 命令并实时捕获输出"""
        if not self.process:
            print("Shell 未启动")
            return

        # 发送命令
        self.process.stdin.write(command + "\n")
        self.process.stdin.flush()

        # 记录输入到历史
        self.history.append(f"输入: {command}")

        # 实时读取输出（最多等待 1 秒）
        output_lines = []
        error_lines = []
        start_time = time.time()

        while time.time() - start_time < 1.0:  # 限制读取时间，避免无限阻塞
            if self.process.stdout.readable():
                line = self.process.stdout.readline().strip()
                if line:
                    output_lines.append(line)
            if self.process.stderr.readable():
                line = self.process.stderr.readline().strip()
                if line:
                    error_lines.append(line)
            # 如果没有更多输出，提前退出
            if not self.process.stdout.readable() and not self.process.stderr.readable():
                break
            time.sleep(0.01)  # 短暂休眠，避免 CPU 占用过高

        # 记录输出到历史
        if output_lines:
            self.history.extend([f"输出: {line}" for line in output_lines])
            print("\n".join(output_lines))
        if error_lines:
            self.history.extend([f"错误: {line}" for line in error_lines])
            print("\n".join(error_lines), file=sys.stderr)

    def call_ai(self, prompt: str):
        context = "\n".join(self.history[-10:])
        full_prompt = f"以下是我的 shell 历史记录：\n{context}\n\n用户请求：{prompt}\n请根据历史和请求提供建议。"
        try:
            response = openai.ChatCompletion.create(
                model="deepseek-chat",  # 替换为你的模型
                messages=[
                    {"role": "system", "content": "你是一个 shell 专家，基于用户的历史记录提供建议。"},
                    {"role": "user", "content": full_prompt}
                ],
                stream=True
            )
            self.stream_ai_response(response)
        except Exception as e:
            print(f"调用 AI 出错: {e}")

    @classmethod
    def stream_ai_response(cls, response: Generator, delay: float = 0.02) -> None:
        accumulated_message = ""
        with Live(Panel("", **cls.PANELS["assistant"], padding=(1, 2)), console=cls.console, refresh_per_second=20) as live:
            for text_chunk in response:
                if text_chunk and hasattr(text_chunk.choices[0].delta, 'content'):
                    text = text_chunk.choices[0].delta.content or ""
                    if text:
                        accumulated_message += text
                        md = Markdown(accumulated_message + "▌")
                        live.update(Panel(md, **cls.PANELS["assistant"], padding=(1, 2)))
                        time.sleep(delay)
            md = Markdown(accumulated_message)
            live.update(Panel(md, **cls.PANELS["assistant"], padding=(1, 2)))

if __name__ == "__main__":
    shell = InteractiveShell()
    shell.start_shell()