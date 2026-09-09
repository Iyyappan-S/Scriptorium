from fastapi import APIRouter
from app.database.mongodb import database

router = APIRouter()


@router.get("/database-test")
def database_test():
    database.list_collection_names()

    return {
        "status": "Connected Successfully",
        "database": database.name
    }
