from enum import Enum
from typing import Any, List, Literal, Optional, Union

from pydantic import BaseModel, Field


class Role(str, Enum):
    """Message role options"""

    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"

class ToolChoice(str, Enum):
    """Tool choice options"""

    NONE = "none"
    AUTO = "auto"
    REQUIRED = "required"

class AgentState(str, Enum):
    """Agent execution states"""

    IDLE = "IDLE"
    RUNNING = "RUNNING"
    FINISHED = "FINISHED"
    ERROR = "ERROR"


TOOL_CHOICE_VALUES = tuple(choice.value for choice in ToolChoice)
ROLE_TYPE = Literal["system", "user", "assistant", "tool"]
ROLE_VALUES = tuple(choice.value for choice in Role)

if __name__ == "__main__":
    # For testing purposes

    tool_choice = ToolChoice.AUTO

    print(tool_choice)
    
    if tool_choice in TOOL_CHOICE_VALUES:
        print("Valid tool choice")
