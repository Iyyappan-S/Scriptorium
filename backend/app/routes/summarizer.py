import os

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from bson import ObjectId

from google import genai

from backend.app.database.mongodb import db


router = APIRouter(
    prefix="/api/summarizer",
    tags=["Paper Summarizer"]
)


class SummarizeRequest(BaseModel):
    paper_id: str


def serialize_value(value):
    if isinstance(value, ObjectId):
        return str(value)

    return value


@router.post("")
async def summarize_paper(request: SummarizeRequest):

    try:

        # -----------------------------------------
        # 1. Validate paper ID
        # -----------------------------------------

        try:
            object_id = ObjectId(request.paper_id)

        except Exception:
            raise HTTPException(
                status_code=400,
                detail="Invalid paper ID."
            )


        # -----------------------------------------
        # 2. Retrieve paper from MongoDB
        # -----------------------------------------

        paper = db.papers.find_one({
            "_id": object_id
        })


        if not paper:

            raise HTTPException(
                status_code=404,
                detail="Research paper not found."
            )


        # -----------------------------------------
        # 3. Extract paper information
        # -----------------------------------------

        title = paper.get(
            "title",
            "Unknown Title"
        )

        authors = paper.get(
            "authors",
            "Unknown Authors"
        )

        year = paper.get(
            "publication_year",
            "N/A"
        )

        abstract = paper.get(
            "abstract",
            ""
        )

        concepts = paper.get(
            "concepts",
            ""
        )

        doi = paper.get(
            "doi",
            ""
        )


        # -----------------------------------------
        # 4. Build research context
        # -----------------------------------------

        paper_context = f"""
TITLE:
{title}

AUTHORS:
{authors}

PUBLICATION YEAR:
{year}

ABSTRACT:
{abstract}

CONCEPTS:
{concepts}

DOI:
{doi}
"""


        # -----------------------------------------
        # 5. Gemini configuration
        # -----------------------------------------

        api_key = os.getenv(
            "GEMINI_API_KEY"
        )


        if not api_key:

            raise HTTPException(
                status_code=500,
                detail="GEMINI_API_KEY is not configured."
            )


        client = genai.Client(
            api_key=api_key
        )


        # -----------------------------------------
        # 6. Academic summarization prompt
        # -----------------------------------------

        prompt = f"""
You are an academic research assistant.

Analyze the following research paper metadata and
produce a clear academic summary.

Do NOT invent facts that are not present in the
provided information.

If the abstract is unavailable, explicitly state
that the abstract was not available and base the
summary only on the available metadata.

Research Paper:

{paper_context}


Return the response using exactly these sections:

1. Overview

2. Research Problem

3. Methodology

4. Key Findings

5. Research Area

6. Limitations

7. Future Research Directions

8. One-Sentence Summary

Keep the explanation suitable for a university
research student.
"""


        # -----------------------------------------
        # 7. Generate AI summary
        # -----------------------------------------

        response = client.models.generate_content(

            model="gemini-2.5-flash",

            contents=prompt
        )


        summary = response.text


        # -----------------------------------------
        # 8. Return result
        # -----------------------------------------

        return {

            "success": True,

            "data": {

                "paper": {

                    "id": serialize_value(
                        paper.get("_id")
                    ),

                    "title": title,

                    "authors": authors,

                    "publication_year": year,

                    "doi": doi
                },

                "summary": summary,

                "agent": "Summarization Agent"

            }

        }


    except HTTPException:

        raise


    except Exception as error:

        print(
            "Summarizer Error:",
            error
        )

        raise HTTPException(

            status_code=500,

            detail=str(error)

        )