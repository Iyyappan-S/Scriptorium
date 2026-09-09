from fastapi import APIRouter
from backend.app.agents.research_agent import ResearchAgent

router = APIRouter()

research_agent = ResearchAgent()


@router.get("/research")
def research(query: str):
    return research_agent.execute(query)