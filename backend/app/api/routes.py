from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.app.agents.orchestrator import OrchestratorAgent


router = APIRouter()

orchestrator = OrchestratorAgent()


class ResearchRequest(BaseModel):
    query: str


@router.post("/research")
def research(request: ResearchRequest):

    query = request.query.strip()

    if not query:
        raise HTTPException(
            status_code=400,
            detail="Query cannot be empty"
        )

    try:
        result = orchestrator.execute(query)
        return result

    except Exception as e:
        print(f"[Research API ERROR] {e}")

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )