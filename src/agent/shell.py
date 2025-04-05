from agent.baseAgent import BaseAgent


class ShellAgent(BaseAgent):
    def __init__(self, llm, memory):
        super().__init__(llm, memory)

    def think(self, input_data: str) -> str:
        return super().think(input_data)
