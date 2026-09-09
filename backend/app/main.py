from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from app.agents.orchestrator import OrchestratorAgent

app = FastAPI(title="AI Academic Research Platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

orchestrator = OrchestratorAgent()

class QueryRequest(BaseModel):
    query: str
    k: Optional[int] = 5
    threshold: Optional[float] = 0.50
    agent_type: Optional[str] = None

class ActionRequest(BaseModel):
    query: str
    papers: List[dict]
    agent_type: str

@app.post("/api/research/ask")
async def ask_research(req: QueryRequest):
    try:
        context = {
            "k": req.k,
            "threshold": req.threshold
        }
        if req.agent_type:
            context["agent_type"] = req.agent_type
            
        result = orchestrator.execute(req.query, context)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
@app.post("/api/research/action")
async def direct_action(req: ActionRequest):
    try:
        context = {
            "agent_type": req.agent_type,
            "papers": req.papers
        }
        result = orchestrator.execute(req.query, context)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
