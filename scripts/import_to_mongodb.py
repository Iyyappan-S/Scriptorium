import os
import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv("backend/.env")

MONGODB_URI = os.getenv("MONGODB_URI")

DATABASE_NAME = "research_platform"
COLLECTION_NAME = "research_papers"

DATASET = "dataset/processed/clean_research_papers.csv"

if not os.path.exists(DATASET):
    print("Dataset not found!")
    exit()

print("Loading dataset...")

df = pd.read_csv(DATASET)

print(f"Records found: {len(df)}")

print("Connecting to MongoDB...")

client = MongoClient(MONGODB_URI)

db = client[DATABASE_NAME]

collection = db[COLLECTION_NAME]

print("Deleting old records...")

collection.delete_many({})

print("Inserting new records...")

records = df.to_dict(orient="records")

collection.insert_many(records)

print("\n================================")
print("Upload Successful!")
print("================================")
print(f"Inserted Records : {len(records)}")
print(f"Database         : {DATABASE_NAME}")
print(f"Collection       : {COLLECTION_NAME}")
