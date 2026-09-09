import pandas as pd
import faiss
import pickle
import os

def validate_dataset():
    df = pd.read_csv("dataset/processed/clean_research_papers.csv")
    total = len(df)
    empty_titles = df['title'].isnull().sum()
    empty_abstracts = df['abstract'].isnull().sum()
    duplicate_titles = df.duplicated(subset=['title']).sum()
    
    print("\nDATASET QUALITY REPORT")
    print("-" * 25)
    print(f"Records: {total}")
    print(f"Abstract coverage: {(1 - empty_abstracts/total) * 100:.2f}%")
    print(f"Duplicate titles: {duplicate_titles}")
    print(f"Empty titles: {empty_titles}")

if __name__ == "__main__":
    validate_dataset()
