from fastapi import APIRouter, HTTPException

from backend.app.agents.orchestrator import OrchestratorAgent


router = APIRouter()

orchestrator = OrchestratorAgent()


@router.get("/ask")
def ask(query: str):

    try:

        query = query.strip()

        if not query:

            raise HTTPException(
                status_code=400,
                detail="Query cannot be empty"
            )

        result = orchestrator.execute(
            query
        )

        return result

    except HTTPException:

        raise

    except Exception as e:

        print(
            f"[Orchestrator ERROR] {str(e)}"
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )