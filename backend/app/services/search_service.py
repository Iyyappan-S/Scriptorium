from pymongo import MongoClient
from backend.app.config.settings import settings

client = MongoClient(settings.MONGODB_URI)

db = client["research_platform"]

collection = db["research_papers"]


def search_papers(query: str, limit: int = 10):

    papers = collection.find(
        {
            "$or": [
                {"title": {"$regex": query, "$options": "i"}},
                {"authors": {"$regex": query, "$options": "i"}},
                {"concepts": {"$regex": query, "$options": "i"}}
            ]
        },
        {
            "_id": 0
        }
    ).limit(limit)

    return list(papers)