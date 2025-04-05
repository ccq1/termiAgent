from rich.panel import Panel
from rich.syntax import Syntax
from rich.markdown import Markdown
from rich.text import Text
from typing import Any, Dict, Iterator, AsyncIterator, Union, Generator
from rich.console import Console
from rich.live import Live
from enums import ROLE_TYPE
import time

class MessageRenderer:
    """消息渲染器类，用于在终端中渲染各种类型的消息"""
    
    # 控制台实例
    console = Console()
    
    # Panel样式配置
    PANELS = {
        "user": {
            "title": "[bold blue]User[/bold blue]",
            "border_style": "blue",
        },
        "assistant": {
            "title": "[bold green]Assistant[/bold green]",
            "border_style": "green",
        },
        "tool_call": {
            "title": "[bold yellow]Tool Call[/bold yellow]",
            "border_style": "yellow",
        },
        "tool_result_success": {
            "title": "[bold green]Success[/bold green]",
            "border_style": "green",
        },
        "tool_result_error": {
            "title": "[bold red]Error[/bold red]",
            "border_style": "red",
        }
    }
    
    # 日志级别样式配置
    LOG_STYLES = {
        "info": "cyan",
        "warning": "yellow",
        "error": "red",
        "debug": "dim white"
    }
   
    @classmethod
    def print_user_input(cls, message: str) -> None:
        """渲染用户输入的消息"""
        panel = Panel(
            message,
            **cls.PANELS["user"],
            padding=(1, 2)
        )
        cls.console.print(panel)

    @classmethod
    def stream_ai_response(cls, response: Generator, delay: float = 0.02) -> None:
        """流式渲染AI的回复消息
        
        Args:
            response: LLM的流式响应生成器，每次yield一段文本
            delay: 每个文本片段的延迟时间（秒）
        """
        accumulated_message = ""
        
        with Live(Panel("", **cls.PANELS["assistant"], padding=(1, 2)), console=cls.console, refresh_per_second=20) as live:
            for text_chunk in response:
                if text_chunk and hasattr(text_chunk.choices[0].delta, 'content'):
                    text = text_chunk.choices[0].delta.content or ""
                    if text:  # 只在有实际内容时更新
                        accumulated_message += text
                        md = Markdown(accumulated_message + "▌",justify="left")
                        live.update(Panel(md, **cls.PANELS["assistant"], padding=(1, 2)))
            
            # 显示最终完整消息（去掉光标）
            md = Markdown(accumulated_message)
            live.update(Panel(md, **cls.PANELS["assistant"], padding=(1, 2)))

    @classmethod
    def print_ai_response(cls, message: str) -> None:
        """渲染AI的完整回复消息（非流式）"""
        md = Markdown(message)
        panel = Panel(
            md,
            **cls.PANELS["assistant"],
            padding=(1, 2)
        )
        cls.console.print(panel)

    @classmethod
    def print_tool_call(cls, tool_name: str, parameters: Dict[str, Any]) -> None:
        """渲染工具调用信息"""
        params_text = "\n".join([f"{k}: {v}" for k, v in parameters.items()])
        content = Text.from_markup(f"[bold]Tool:[/bold] {tool_name}\n[bold]Parameters:[/bold]\n{params_text}")
        
        panel = Panel(
            content,
            **cls.PANELS["tool_call"],
            padding=(1, 2)
        )
        cls.console.print(panel)

    @classmethod
    def stream_tool_result(cls, result_iterator: Iterator[str], success: bool = True) -> None:
        """流式渲染工具调用的返回结果
        
        Args:
            result_iterator: 结果字符串的迭代器
            success: 是否成功
        """
        panel_style = "tool_result_success" if success else "tool_result_error"
        accumulated_result = ""
        
        with Live(
            Panel("", **cls.PANELS[panel_style], padding=(1, 2)),
            console=cls.console,
            refresh_per_second=20
        ) as live:
            for chunk in result_iterator:
                accumulated_result += chunk
                content = Text(accumulated_result + "▌")
                live.update(
                    Panel(content, **cls.PANELS[panel_style], padding=(1, 2))
                )
                time.sleep(0.02)
            
            # 最终显示完整结果（不带光标）
            content = Text(accumulated_result)
            live.update(
                Panel(content, **cls.PANELS[panel_style], padding=(1, 2))
            )

    @classmethod
    def print_tool_result(cls, result: Any, success: bool = True) -> None:
        """渲染工具调用的完整返回结果（非流式）"""
        result_str = str(result) if isinstance(result, str) else repr(result)
        panel_style = "tool_result_success" if success else "tool_result_error"
        
        if "```" in result_str:
            content = Syntax(result_str, "python", theme="monokai", line_numbers=True)
        else:
            content = Text(result_str)
        
        panel = Panel(
            content,
            **cls.PANELS[panel_style],
            padding=(1, 2)
        )
        cls.console.print(panel)

    @classmethod
    def print_system_log(cls, message: str, level: str = "info") -> None:
        """渲染系统日志信息"""
        style = cls.LOG_STYLES.get(level, "white")
        cls.console.print(f"[{style}][{level.upper()}] {message}[/{style}]")

    @staticmethod
    def shell_print(self,role: ROLE_TYPE, message: str, **kwargs) -> None:
        """渲染shell消息"""
        if role == "user":
            self.print_user_input(message)
        elif role == "assistant":
            self.print_ai_response(message)
        elif role == "tool":
            self.print_tool_call(message, **kwargs)

if __name__ == "__main__":
    from llm import LLM
    llm = LLM()
    MessageRenderer.stream_ai_response(llm.chat_llm("在本地文件夹找到enmus.py这个文件"))