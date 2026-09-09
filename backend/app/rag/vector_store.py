import faiss
import numpy as np
import pickle
import os
import math


# ============================================================
# BACKEND DIRECTORY
# ============================================================

BACKEND_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)


# ============================================================
# FAISS STORAGE DIRECTORY
# ============================================================

FAISS_DIR = os.path.join(
    BACKEND_DIR,
    "vector_store",
    "faiss_index"
)


INDEX_PATH = os.path.join(
    FAISS_DIR,
    "index.faiss"
)


METADATA_PATH = os.path.join(
    FAISS_DIR,
    "metadata.pkl"
)


# ============================================================
# JSON SAFE VALUE CONVERTER
# ============================================================

def make_json_safe(value):
    """
    Recursively converts MongoDB / NumPy values
    into JSON-safe Python values.
    """

    # --------------------------------------------------------
    # MongoDB ObjectId
    # --------------------------------------------------------

    if value.__class__.__name__ == "ObjectId":
        return str(value)

    # --------------------------------------------------------
    # Dictionary
    # --------------------------------------------------------

    if isinstance(value, dict):

        return {
            str(key): make_json_safe(val)
            for key, val in value.items()
        }

    # --------------------------------------------------------
    # List
    # --------------------------------------------------------

    if isinstance(value, list):

        return [
            make_json_safe(item)
            for item in value
        ]

    # --------------------------------------------------------
    # Tuple
    # --------------------------------------------------------

    if isinstance(value, tuple):

        return [
            make_json_safe(item)
            for item in value
        ]

    # --------------------------------------------------------
    # NumPy integer
    # --------------------------------------------------------

    if isinstance(value, np.integer):

        return int(value)

    # --------------------------------------------------------
    # NumPy floating point
    # --------------------------------------------------------

    if isinstance(value, np.floating):

        value = float(value)

        if not math.isfinite(value):
            return None

        return value

    # --------------------------------------------------------
    # Normal Python float
    # --------------------------------------------------------

    if isinstance(value, float):

        if not math.isfinite(value):
            return None

        return value

    # --------------------------------------------------------
    # NumPy boolean
    # --------------------------------------------------------

    if isinstance(value, np.bool_):

        return bool(value)

    # --------------------------------------------------------
    # Everything else
    # --------------------------------------------------------

    return value


# ============================================================
# VECTOR STORE
# ============================================================

class VectorStore:

    def __init__(self, dimension=384):

        self.dimension = dimension

        self.index = faiss.IndexFlatL2(
            dimension
        )

        self.metadata = []


    # ========================================================
    # ADD DOCUMENT
    # ========================================================

    def add(self, embedding, document):

        vector = np.array(
            [embedding],
            dtype=np.float32
        )

        self.index.add(vector)

        safe_document = make_json_safe(document)

        self.metadata.append(
            safe_document
        )


    # ========================================================
    # SAVE INDEX
    # ========================================================

    def save(self):

        os.makedirs(
            FAISS_DIR,
            exist_ok=True
        )

        faiss.write_index(
            self.index,
            INDEX_PATH
        )

        with open(
            METADATA_PATH,
            "wb"
        ) as f:

            pickle.dump(
                self.metadata,
                f
            )

        print("FAISS index saved:")
        print(INDEX_PATH)

        print("Metadata saved:")
        print(METADATA_PATH)


    # ========================================================
    # LOAD INDEX
    # ========================================================

    def load(self):

        if not os.path.exists(INDEX_PATH):

            raise FileNotFoundError(
                f"FAISS index not found: {INDEX_PATH}"
            )


        if not os.path.exists(METADATA_PATH):

            raise FileNotFoundError(
                f"FAISS metadata not found: {METADATA_PATH}"
            )


        self.index = faiss.read_index(
            INDEX_PATH
        )


        with open(
            METADATA_PATH,
            "rb"
        ) as f:

            self.metadata = pickle.load(f)


        print(
            f"FAISS index loaded successfully: "
            f"{self.index.ntotal} vectors"
        )


    # ========================================================
    # SEARCH
    # ========================================================

    def search(
        self,
        embedding,
        k=5
    ):

        # ----------------------------------------------------
        # Convert embedding
        # ----------------------------------------------------

        vector = np.array(
            [embedding],
            dtype=np.float32
        )


        # ----------------------------------------------------
        # FAISS search
        # ----------------------------------------------------

        distances, indices = self.index.search(
            vector,
            k
        )


        results = []


        # ----------------------------------------------------
        # Process results
        # ----------------------------------------------------

        for idx, distance in zip(
            indices[0],
            distances[0]
        ):

            # Ignore invalid index

            if idx == -1:
                continue


            # ------------------------------------------------
            # Get metadata
            # ------------------------------------------------

            document = self.metadata[idx]


            # ------------------------------------------------
            # Convert entire document to JSON-safe format
            # ------------------------------------------------

            document = make_json_safe(
                document
            )


            # ------------------------------------------------
            # Clean distance
            # ------------------------------------------------

            distance = float(distance)


            if not math.isfinite(distance):

                distance = 999999.0


            # ------------------------------------------------
            # Add result
            # ------------------------------------------------

            results.append({

                "document": document,

                "distance": distance

            })


        return results
