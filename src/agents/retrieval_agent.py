from pathlib import Path
from typing import Dict, Any, List
import pickle

import faiss
from sentence_transformers import SentenceTransformer


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

VECTOR_STORE_DIR = PROJECT_ROOT / "data" / "vector_store"


FAISS_INDEX_PATH = (
    VECTOR_STORE_DIR / "faq_faiss.index"
)

METADATA_PATH = (
    VECTOR_STORE_DIR / "faq_metadata.pkl"
)

RAG_CONFIG_PATH = (
    VECTOR_STORE_DIR / "rag_config.pkl"
)


# ============================================================
# CHECK FILES
# ============================================================

required_files = [
    FAISS_INDEX_PATH,
    METADATA_PATH,
    RAG_CONFIG_PATH
]

for file_path in required_files:

    if not file_path.exists():

        raise FileNotFoundError(
            f"Required RAG file not found: {file_path}"
        )


# ============================================================
# LOAD FAISS INDEX
# ============================================================

print("Loading FAISS index...")

index = faiss.read_index(
    str(FAISS_INDEX_PATH)
)

print(
    f"FAISS index loaded. "
    f"Total vectors: {index.ntotal}"
)


# ============================================================
# LOAD METADATA
# ============================================================

print("Loading FAQ metadata...")

with open(
    METADATA_PATH,
    "rb"
) as f:

    metadata = pickle.load(f)


print(
    f"Metadata loaded. "
    f"Total records: {len(metadata)}"
)


# ============================================================
# LOAD RAG CONFIG
# ============================================================

with open(
    RAG_CONFIG_PATH,
    "rb"
) as f:

    rag_config = pickle.load(f)


# ============================================================
# LOAD EMBEDDING MODEL
# ============================================================

embedding_model_name = rag_config.get(
    "embedding_model",
    "sentence-transformers/all-MiniLM-L6-v2"
)

print(
    f"Loading embedding model: "
    f"{embedding_model_name}"
)

embedding_model = SentenceTransformer(
    embedding_model_name
)

print("Embedding model loaded successfully.")


# ============================================================
# RETRIEVE FAQ DOCUMENTS
# ============================================================

def retrieve_documents(
    query: str,
    top_k: int = 5
) -> List[Dict[str, Any]]:
    """
    Retrieve the most relevant FAQ documents
    from the FAISS vector database.

    Parameters
    ----------
    query : str
        Customer support query.

    top_k : int
        Number of documents to retrieve.

    Returns
    -------
    list
        Relevant FAQ documents with similarity scores.
    """

    if not query or not query.strip():

        return []


    # --------------------------------------------------------
    # Create query embedding
    # --------------------------------------------------------

    query_embedding = embedding_model.encode(
        [query],
        convert_to_numpy=True,
        normalize_embeddings=True
    )


    # FAISS expects float32
    query_embedding = query_embedding.astype(
        "float32"
    )


    # --------------------------------------------------------
    # Limit top_k
    # --------------------------------------------------------

    top_k = min(
        top_k,
        index.ntotal
    )


    # --------------------------------------------------------
    # Search FAISS
    # --------------------------------------------------------

    scores, indices = index.search(
        query_embedding,
        top_k
    )


    # --------------------------------------------------------
    # Prepare results
    # --------------------------------------------------------

    results = []


    for score, idx in zip(
        scores[0],
        indices[0]
    ):

        # FAISS can return -1
        if idx == -1:
            continue


        # Get metadata
        item = metadata[idx]


        # ----------------------------------------------------
        # Handle metadata format
        # ----------------------------------------------------

        result = {

            "score": float(score),

            "faq_id": item.get(
                "faq_id",
                ""
            ),

            "category": item.get(
                "category",
                ""
            ),

            "text": item.get(
                "text",
                ""
            )
        }


        # Keep question/answer if present
        if "question" in item:

            result["question"] = item[
                "question"
            ]

        if "answer" in item:

            result["answer"] = item[
                "answer"
            ]


        results.append(result)


    return results


# ============================================================
# RETRIEVAL AGENT
# ============================================================

class RetrievalAgent:
    """
    Retrieval Agent

    Responsibilities:

    1. Receive ticket state
    2. Use cleaned ticket text as query
    3. Search FAQ vector database
    4. Retrieve relevant FAQ documents
    5. Add retrieved documents to ticket state
    """

    def __init__(
        self,
        top_k: int = 5
    ):

        self.name = "RetrievalAgent"

        self.top_k = top_k


    # --------------------------------------------------------
    # PROCESS
    # --------------------------------------------------------

    def process(
        self,
        ticket_state: Dict[str, Any]
    ) -> Dict[str, Any]:

        # ----------------------------------------------------
        # Validate state
        # ----------------------------------------------------

        if not ticket_state:

            return {

                "status": "error",

                "error":
                    "Ticket state is required.",

                "agent":
                    self.name
            }


        # ----------------------------------------------------
        # Get cleaned text
        # ----------------------------------------------------

        query = ticket_state.get(
            "cleaned_text"
        )


        if not query:

            return {

                "status": "error",

                "error":
                    "cleaned_text is missing.",

                "agent":
                    self.name
            }


        # ----------------------------------------------------
        # Retrieve documents
        # ----------------------------------------------------

        retrieved_documents = retrieve_documents(
            query=query,
            top_k=self.top_k
        )


        # ----------------------------------------------------
        # Update ticket state
        # ----------------------------------------------------

        ticket_state[
            "retrieved_documents"
        ] = retrieved_documents


        ticket_state[
            "retrieval_completed"
        ] = True


        ticket_state[
            "retrieval_agent"
        ] = self.name


        return ticket_state


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    agent = RetrievalAgent(
        top_k=5
    )


    # Simulated output from Classification Agent

    test_ticket_state = {

        "status": "success",

        "cleaned_text":
            "My order #12345 arrived damaged. "
            "I want a replacement for my laptop.",

        "intent":
            "damaged_product",

        "sentiment":
            "Negative",

        "entities": {

            "order_id":
                "12345",

            "product":
                ["laptop"]
        },

        "category":
            "Product Issue",

        "priority":
            "High",

        "classification_completed":
            True
    }


    # --------------------------------------------------------
    # Run Retrieval Agent
    # --------------------------------------------------------

    result = agent.process(
        test_ticket_state
    )


    # --------------------------------------------------------
    # Display results
    # --------------------------------------------------------

    print("\n")
    print("=" * 70)
    print("RETRIEVAL AGENT RESULT")
    print("=" * 70)


    print(
        "\nRetrieval completed:",
        result.get(
            "retrieval_completed"
        )
    )


    print(
        "\nRetrieved documents:"
    )


    for i, document in enumerate(
        result.get(
            "retrieved_documents",
            []
        ),
        start=1
    ):

        print("\n" + "-" * 60)

        print(
            f"Result {i}"
        )

        print(
            "FAQ ID:",
            document.get(
                "faq_id"
            )
        )

        print(
            "Score:",
            round(
                document.get(
                    "score",
                    0
                ),
                4
            )
        )

        print(
            "Category:",
            document.get(
                "category"
            )
        )

        print(
            "Text:",
            document.get(
                "text"
            )[:500]
        )

    print("\n")
    print("=" * 70)
