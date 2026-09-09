from pymongo import MongoClient

from app.config.settings import settings


client = MongoClient(settings.MONGODB_URI)

db = client[settings.DATABASE_NAME]


def get_database():
    return db
