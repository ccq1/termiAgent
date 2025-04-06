from abc import ABC, abstractmethod
from typing import List, Dict, Any
from src.llm import LLM
from pydantic import BaseModel, Field



class BaseAgent(ABC, BaseModel):
    
    def __init__(self, llm: Any, memory: Dict[str, Any]):
        """
        初始化 BaseAgent。
        
        参数:
            llm: 大语言模型实例，作为 Agent 的核心推理能力（大脑）。
            memory: 记忆存储，用于保存上下文或历史信息，可以是字典或其他数据结构。
        """
        self.llm : LLM = Field(default_factory=llm)  # LLM 实例
        self.memory : Dict[str, Any] = Field(default_factory=memory)  # 记忆存储
        self.tools : Dict[str, Any] = Field(default_factory=dict)  # 工具集，用于存储工具的实例
       

    @abstractmethod
    def think(self, input_data: str) -> str:
        """
        使用 LLM 进行思考和推理，生成响应。
        
        参数:
            input_data: 输入的数据或问题（字符串形式）。
        
        返回:
            思考后的输出结果（字符串形式）。
        """
        pass

    @abstractmethod
    def remember(self, key: str, value: Any) -> None:
        """
        将信息存储到记忆中。
        
        参数:
            key: 记忆的键，用于标识存储的信息。
            value: 存储的具体信息，可以是任意类型。
        """
        pass

    @abstractmethod
    def recall(self, key: str) -> Any:
        """
        从记忆中检索信息。
        
        参数:
            key: 要检索的记忆的键。
        
        返回:
            对应的记忆值，如果不存在则返回 None 或抛出异常。
        """
        pass

    @abstractmethod
    def perform_action(self, action_name: str, params: Dict[str, Any]) -> Any:
        """
        执行特定的行为（工具调用或功能调用）。
        
        参数:
            action_name: 要执行的行为名称（例如 "search", "generate_image"）。
            params: 执行行为所需的参数（字典形式）。
        
        返回:
            行为执行的结果。
        """
        pass

    @abstractmethod
    def get_available_actions(self) -> List[str]:
        """
        获取当前 Agent 支持的所有行为列表。
        
        返回:
            可用的行为名称列表。
        """
        pass

# 示例实现（可选）
class SimpleAgent(BaseAgent):
    def __init__(self, llm, memory):
        super().__init__(llm, memory)
        self.actions = {
            "say_hello": lambda params: f"你好，{params.get('name', '朋友')}！",
            "add_numbers": lambda params: params["a"] + params["b"]
        }

    def think(self, input_data: str) -> str:
        return self.llm.process(input_data)  # 假设 llm 有 process 方法

    def remember(self, key: str, value: Any) -> None:
        self.memory[key] = value

    def recall(self, key: str) -> Any:
        return self.memory.get(key)

    def perform_action(self, action_name: str, params: Dict[str, Any]) -> Any:
        action = self.actions.get(action_name)
        if action:
            return action(params)
        raise ValueError(f"未知的行为: {action_name}")

    def get_available_actions(self) -> List[str]:
        return list(self.actions.keys())

# 使用示例
if __name__ == "__main__":
    # 假设有一个简单的 LLM 和 memory
    class DummyLLM:
        def process(self, text):
            return f"处理: {text}"

    llm = DummyLLM()
    memory = {}
    agent = SimpleAgent(llm, memory)

    # 测试功能
    print(agent.think("你好吗？"))  # 输出: 处理: 你好吗？
    agent.remember("user_name", "小明")
    print(agent.recall("user_name"))  # 输出: 小