from pathlib import Path


# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent


# ============================================================
# DATA PATHS
# ============================================================

DATA_DIR = PROJECT_ROOT / "data"

RAW_DATA_DIR = DATA_DIR / "raw"

PROCESSED_DATA_DIR = DATA_DIR / "processed"

KNOWLEDGE_BASE_DIR = DATA_DIR / "knowledge_base"

VECTOR_STORE_DIR = DATA_DIR / "vector_store"


# ============================================================
# MODEL PATHS
# ============================================================

MODELS_DIR = PROJECT_ROOT / "models"

TICKET_CATEGORY_MODEL = MODELS_DIR / "ticket_category_model.pkl"

TICKET_CATEGORY_TFIDF = MODELS_DIR / "ticket_category_tfidf.pkl"

PRIORITY_MODEL = MODELS_DIR / "priority_model.pkl"

PRIORITY_TFIDF = MODELS_DIR / "priority_tfidf.pkl"

SENTIMENT_MODEL = MODELS_DIR / "sentiment_model.pkl"

SENTIMENT_WORD_TFIDF = MODELS_DIR / "sentiment_word_tfidf.pkl"

SENTIMENT_CHAR_TFIDF = MODELS_DIR / "sentiment_char_tfidf.pkl"


# ============================================================
# RAG / VECTOR STORE
# ============================================================

FAQ_FAISS_INDEX = VECTOR_STORE_DIR / "faq_faiss.index"

FAQ_METADATA = VECTOR_STORE_DIR / "faq_metadata.pkl"

RAG_CONFIG = VECTOR_STORE_DIR / "rag_config.pkl"


# ============================================================
# EMBEDDING MODEL
# ============================================================

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


# ============================================================
# OLLAMA / LLM CONFIGURATION
# ============================================================

OLLAMA_URL = "http://localhost:11434/api/generate"

OLLAMA_MODEL = "gemma3:4b"

LLM_TEMPERATURE = 0.2


# ============================================================
# RAG CONFIGURATION
# ============================================================

TOP_K = 5

RETRIEVAL_SCORE_THRESHOLD = 0.35


# ============================================================
# CLASSIFICATION CONFIGURATION
# ============================================================

CATEGORY_CONFIDENCE_THRESHOLD = 0.60

PRIORITY_CONFIDENCE_THRESHOLD = 0.60


# ============================================================
# LOGGING
# ============================================================

LOGS_DIR = PROJECT_ROOT / "logs"

TICKET_LOG_FILE = LOGS_DIR / "ticket_logs.jsonl"
