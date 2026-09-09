from pydantic import BaseModel
from typing import List, Optional


class ResearchPaper(BaseModel):
    title: str
    authors: List[str]
    abstract: Optional[str] = ""
    year: int
    doi: Optional[str] = ""
    keywords: List[str] = []
