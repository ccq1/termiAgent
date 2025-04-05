from pydantic import BaseModel,Field
from typing import List, Optional, Literal
from enums import TOOL_CHOICE_VALUES,ToolChoice, ROLE_TYPE

class Function(BaseModel):
    name: str
    arguments: str


class ToolCall(BaseModel):
    """Represents a tool/function call in a message"""

    id: str
    type: str = "function"
    function: Function

class Message(BaseModel):
    role: ROLE_TYPE
    content: str
    tool_calls: Optional[List[ToolCall]] = None




# 示例用法
if __name__ == "__main__":
    # 定义 get_weather 工具
   
    pass