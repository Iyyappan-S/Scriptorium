from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseAgent(ABC):
    def __init__(self, name: str):
        self.name = name
        
    @abstractmethod
    def execute(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        pass
