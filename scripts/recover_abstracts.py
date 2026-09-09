import os
import time
import pandas as pd
import requests


# ============================================================
# CONFIGURATION
# ============================================================

INPUT_FILE = "dataset/raw/openalex_research_papers.csv"

OUTPUT_FILE = "dataset/processed/recovered_research_papers.csv"

API_URL = "https://api.openalex.org/works/{}"

REQUEST_DELAY = 0.1

TIMEOUT = 30

SAVE_EVERY = 100


# ============================================================
# ABSTRACT RECONSTRUCTION
# ============================================================

def reconstruct_abstract(inverted_index):

    if not inverted_index:
        return ""

    positions = []

    for word, indexes in inverted_index.items():

        for index in indexes:

            positions.append(
                (index, word)
            )

    positions.sort(
        key=lambda x: x[0]
    )

    abstract = " ".join(
        word
        for _, word in positions
    )

    return abstract.strip()


# ============================================================
# OPENALEX ID EXTRACTION
# ============================================================

def extract_work_id(openalex_id):

    if not openalex_id:
        return None

    openalex_id = str(openalex_id).strip()

    return openalex_id.rstrip("/").split("/")[-1]


# ============================================================
# FETCH ABSTRACT
# ============================================================

def fetch_abstract(work_id):

    if not work_id:
        return ""

    url = API_URL.format(work_id)

    try:

        response = requests.get(
            url,
            timeout=TIMEOUT
        )

        if response.status_code != 200:

            print(
                f"[API ERROR] {work_id} "
                f"Status: {response.status_code}"
            )

            return ""

        data = response.json()

        inverted_index = data.get(
            "abstract_inverted_index"
        )

        return reconstruct_abstract(
            inverted_index
        )

    except Exception as e:

        print(
            f"[REQUEST ERROR] {work_id}: {e}"
        )

        return ""


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 60)
    print("PHASE 21 - ABSTRACT RECOVERY")
    print("=" * 60)

    if not os.path.exists(INPUT_FILE):

        print(
            f"Input dataset not found: {INPUT_FILE}"
        )

        return

    print("\nLoading dataset...")

    df = pd.read_csv(
        INPUT_FILE
    )

    print(
        f"Total records: {len(df)}"
    )

    # --------------------------------------------------------
    # Ensure abstract column exists
    # --------------------------------------------------------

    if "abstract" not in df.columns:

        df["abstract"] = ""

    df["abstract"] = (
        df["abstract"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    # --------------------------------------------------------
    # Statistics
    # --------------------------------------------------------

    existing_abstracts = (
        df["abstract"]
        .ne("")
        .sum()
    )

    print(
        f"Existing abstracts: {existing_abstracts}"
    )

    # --------------------------------------------------------
    # Resume support
    # --------------------------------------------------------

    recovered = 0
    failed = 0
    skipped = 0

    total = len(df)

    print("\nStarting abstract recovery...\n")

    for index in range(total):

        current_abstract = df.at[
            index,
            "abstract"
        ]

        # ----------------------------------------------------
        # Skip existing abstracts
        # ----------------------------------------------------

        if (
            isinstance(current_abstract, str)
            and current_abstract.strip()
        ):

            skipped += 1

            continue

        # ----------------------------------------------------
        # Extract OpenAlex ID
        # ----------------------------------------------------

        work_id = extract_work_id(
            df.at[index, "id"]
        )

        if not work_id:

            failed += 1

            continue

        # ----------------------------------------------------
        # Fetch abstract
        # ----------------------------------------------------

        abstract = fetch_abstract(
            work_id
        )

        if abstract:

            df.at[
                index,
                "abstract"
            ] = abstract

            recovered += 1

        else:

            failed += 1

        # ----------------------------------------------------
        # Progress
        # ----------------------------------------------------

        processed = (
            recovered +
            failed +
            skipped
        )

        if processed % 25 == 0:

            print(
                f"Progress: "
                f"{processed}/{total} | "
                f"Recovered: {recovered} | "
                f"Failed: {failed}"
            )

        # ----------------------------------------------------
        # Periodic save
        # ----------------------------------------------------

        if processed % SAVE_EVERY == 0:

            os.makedirs(
                os.path.dirname(
                    OUTPUT_FILE
                ),
                exist_ok=True
            )

            df.to_csv(
                OUTPUT_FILE,
                index=False
            )

            print(
                f"[CHECKPOINT] "
                f"Saved at {processed} records."
            )

        time.sleep(
            REQUEST_DELAY
        )

    # ========================================================
    # FINAL SAVE
    # ========================================================

    os.makedirs(
        os.path.dirname(
            OUTPUT_FILE
        ),
        exist_ok=True
    )

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    # ========================================================
    # FINAL STATISTICS
    # ========================================================

    final_abstracts = (
        df["abstract"]
        .fillna("")
        .astype(str)
        .str.strip()
        .ne("")
        .sum()
    )

    coverage = (
        final_abstracts /
        len(df) *
        100
    )

    print("\n")
    print("=" * 60)
    print("ABSTRACT RECOVERY COMPLETED")
    print("=" * 60)

    print(
        f"Total records       : {len(df)}"
    )

    print(
        f"Recovered abstracts : {recovered}"
    )

    print(
        f"Skipped abstracts   : {skipped}"
    )

    print(
        f"Failed records      : {failed}"
    )

    print(
        f"Final abstracts     : {final_abstracts}"
    )

    print(
        f"Abstract coverage   : {coverage:.2f}%"
    )

    print(
        f"\nSaved to:\n{OUTPUT_FILE}"
    )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()