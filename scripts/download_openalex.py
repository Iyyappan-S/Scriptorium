import requests
import pandas as pd
import os
import time


# ============================================================
# CONFIGURATION
# ============================================================

API_URL = "https://api.openalex.org/works"

OUTPUT_FILE = "dataset/raw/openalex_research_papers.csv"

TOTAL_RECORDS = 10000
PER_PAGE = 200

os.makedirs("dataset/raw", exist_ok=True)


# ============================================================
# ABSTRACT RECONSTRUCTION
# ============================================================

def reconstruct_abstract(inverted_index):

    if not inverted_index:
        return ""

    words = []

    for word, positions in inverted_index.items():

        for position in positions:

            words.append(
                (position, word)
            )

    words.sort(
        key=lambda x: x[0]
    )

    return " ".join(
        word
        for _, word in words
    )


# ============================================================
# DOWNLOAD
# ============================================================

def download_papers():

    papers = []

    cursor = "*"

    print("Starting OpenAlex download...")
    print(f"Target records: {TOTAL_RECORDS}")

    while len(papers) < TOTAL_RECORDS:

        params = {
            "filter": "has_abstract:true",
            "per-page": PER_PAGE,
            "cursor": cursor
        }

        print(
            f"Downloading records "
            f"{len(papers) + 1} - "
            f"{min(len(papers) + PER_PAGE, TOTAL_RECORDS)}"
        )

        response = requests.get(
            API_URL,
            params=params,
            timeout=60
        )

        response.raise_for_status()

        data = response.json()

        results = data.get(
            "results",
            []
        )

        if not results:

            print(
                "No more records returned."
            )

            break

        for work in results:

            if len(papers) >= TOTAL_RECORDS:
                break

            abstract = reconstruct_abstract(
                work.get(
                    "abstract_inverted_index"
                )
            )

            authors = []

            for authorship in work.get(
                "authorships",
                []
            ):

                author = authorship.get(
                    "author"
                )

                if author:

                    name = author.get(
                        "display_name"
                    )

                    if name:
                        authors.append(name)

            concepts = []

            for concept in work.get(
                "concepts",
                []
            ):

                name = concept.get(
                    "display_name"
                )

                if name:
                    concepts.append(name)

            papers.append({

                "id": work.get(
                    "id",
                    ""
                ),

                "title": work.get(
                    "title",
                    ""
                ),

                "abstract": abstract,

                "authors": ", ".join(
                    authors
                ),

                "publication_year": work.get(
                    "publication_year"
                ),

                "doi": work.get(
                    "doi",
                    ""
                ),

                "cited_by_count": work.get(
                    "cited_by_count",
                    0
                ),

                "concepts": ", ".join(
                    concepts
                )
            })

        meta = data.get(
            "meta",
            {}
        )

        cursor = meta.get(
            "next_cursor"
        )

        if not cursor:

            print(
                "OpenAlex returned no next cursor."
            )

            break

        time.sleep(0.2)


    # ========================================================
    # SAVE
    # ========================================================

    df = pd.DataFrame(
        papers
    )

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print()
    print(
        "=========================================="
    )
    print(
        "OpenAlex download completed"
    )
    print(
        "=========================================="
    )

    print(
        f"Records downloaded : {len(df)}"
    )

    abstract_count = (
        df["abstract"]
        .fillna("")
        .astype(str)
        .str.strip()
        .ne("")
        .sum()
    )

    print(
        f"Records with abstract : {abstract_count}"
    )

    print(
        f"Abstract coverage : "
        f"{abstract_count / len(df) * 100:.2f}%"
    )

    print(
        f"Saved to : {OUTPUT_FILE}"
    )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    download_papers()