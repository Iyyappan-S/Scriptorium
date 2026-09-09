import pandas as pd
import os

INPUT_FILE = "dataset/raw/openalex_research_papers.csv"
OUTPUT_FILE = "dataset/processed/clean_research_papers.csv"

# ----------------------------------------
# Check dataset exists
# ----------------------------------------

if not os.path.exists(INPUT_FILE):
    print("Dataset not found!")
    exit()

print("Loading dataset...")

df = pd.read_csv(INPUT_FILE)

print(f"Original Records : {len(df)}")

# ----------------------------------------
# Remove Duplicate Papers
# ----------------------------------------

df.drop_duplicates(subset=["title"], inplace=True)

print(f"After Removing Duplicates : {len(df)}")

# ----------------------------------------
# Fill Missing Values
# ----------------------------------------

df["title"] = df["title"].fillna("Unknown Title")
df["authors"] = df["authors"].fillna("Unknown Author")
df["abstract"] = df["abstract"].fillna("")
df["doi"] = df["doi"].fillna("")
df["concepts"] = df["concepts"].fillna("")

# ----------------------------------------
# Clean Text Columns
# ----------------------------------------

text_columns = [
    "title",
    "authors",
    "abstract",
    "doi",
    "concepts"
]

for column in text_columns:

    df[column] = (
        df[column]
        .astype(str)
        .str.replace("\n", " ", regex=False)
        .str.replace("\r", " ", regex=False)
        .str.strip()
    )

# ----------------------------------------
# Publication Year Cleaning
# ----------------------------------------

df["publication_year"] = pd.to_numeric(
    df["publication_year"],
    errors="coerce"
)

df["publication_year"] = (
    df["publication_year"]
    .fillna(0)
    .astype(int)
)

# Remove invalid years

df = df[
    (df["publication_year"] >= 1950) &
    (df["publication_year"] <= 2035)
]

# ----------------------------------------
# Citation Count Cleaning
# ----------------------------------------

df["cited_by_count"] = pd.to_numeric(
    df["cited_by_count"],
    errors="coerce"
)

df["cited_by_count"] = (
    df["cited_by_count"]
    .fillna(0)
    .astype(int)
)

# ----------------------------------------
# Reset Index
# ----------------------------------------

df.reset_index(drop=True, inplace=True)

# ----------------------------------------
# Save Clean Dataset
# ----------------------------------------

os.makedirs("dataset/processed", exist_ok=True)

df.to_csv(OUTPUT_FILE, index=False)

print("\nDataset Cleaning Completed Successfully!\n")

print(f"Final Records : {len(df)}")
print(f"Saved File    : {OUTPUT_FILE}")

print("\nPreview:\n")

print(df.head())