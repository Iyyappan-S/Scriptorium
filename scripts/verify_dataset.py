import pandas as pd
import os

FILE_PATH = "dataset/raw/openalex_research_papers.csv"

if not os.path.exists(FILE_PATH):
    print("Dataset not found!")
    exit()

df = pd.read_csv(FILE_PATH)

print("=" * 50)
print("DATASET INFORMATION")
print("=" * 50)

print(f"Total Papers : {len(df)}")
print(f"Total Columns: {len(df.columns)}")

print("\nColumns:")
print(df.columns.tolist())

print("\nMissing Values:")
print(df.isnull().sum())

print("\nFirst 5 Papers:")
print(df.head())

print("\nDuplicate Papers:", df.duplicated().sum())