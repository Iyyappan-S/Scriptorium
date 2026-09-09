from abc import ABC, abstractmethod
from datetime import datetime


class BaseAgent(ABC):
    """
    Base class for all AI Agents.

    Every agent (Research, Summary, Citation, etc.)
    will inherit from this class.
    """

    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.created_at = datetime.now()

    def get_agent_name(self):
        return self.agent_name

    def log(self, message: str):
        print(f"[{self.agent_name}] {message}")

    @abstractmethod
    def execute(self, query):
        """
        Every AI Agent must implement this method.
        """
        pass
