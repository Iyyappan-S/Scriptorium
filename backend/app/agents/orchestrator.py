from typing import Dict, Any
from .research import ResearchAgent
from .comparison import ComparisonAgent
from .summary import SummaryAgent
from .citation import CitationAgent

class OrchestratorAgent:
    def __init__(self):
        self.agents = {
            "research": ResearchAgent(),
            "comparison": ComparisonAgent(),
            "summary": SummaryAgent(),
            "citation": CitationAgent()
        }

    def _classify_query(self, query: str) -> str:
        q = query.lower()
        if "compare" in q or "difference" in q:
            return "comparison"
        elif "summarize" in q or "summary" in q:
            return "summary"
        elif "cite" in q or "citation" in q:
            return "citation"
        else:
            return "research"

    def execute(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        agent_type = "research"
        if context and "agent_type" in context:
            agent_type = context["agent_type"]
        else:
            agent_type = self._classify_query(query)
            
        agent = self.agents.get(agent_type, self.agents["research"])
        return agent.execute(query, context)