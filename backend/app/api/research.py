from fastapi import APIRouter, HTTPException

from app.schemas.research import ResearchQuery
from app.agents.orchestrator import OrchestratorAgent


router = APIRouter(
    prefix="/api/research",
    tags=["Research"]
)


orchestrator = OrchestratorAgent()


@router.post("/ask")
def ask_research(request: ResearchQuery):

    try:

        if not request.query.strip():
            raise HTTPException(
                status_code=400,
                detail="Query cannot be empty"
            )

        result = orchestrator.execute(
            request.query
        )

        return result

    except HTTPException:
        raise

    except Exception as e:

        print(f"[Research API ERROR] {e}")

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
