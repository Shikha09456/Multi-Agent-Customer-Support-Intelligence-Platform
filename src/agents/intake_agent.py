from pathlib import Path
import re
from typing import Dict, Any

import joblib
from scipy.sparse import hstack


# ============================================================
# PROJECT PATHS
# ============================================================

# Project root:
# Multi-Agent-Customer-Support-Intelligence-Platform/

PROJECT_ROOT = Path(__file__).resolve().parents[2]

MODELS_DIR = PROJECT_ROOT / "models"


# ============================================================
# MODEL PATHS
# ============================================================

SENTIMENT_MODEL_PATH = MODELS_DIR / "sentiment_model.pkl"

SENTIMENT_WORD_TFIDF_PATH = (
    MODELS_DIR / "sentiment_word_tfidf.pkl"
)

SENTIMENT_CHAR_TFIDF_PATH = (
    MODELS_DIR / "sentiment_char_tfidf.pkl"
)


# ============================================================
# LOAD SENTIMENT MODEL + VECTORIZERS
# ============================================================

print("Loading sentiment model...")

sentiment_model = joblib.load(
    SENTIMENT_MODEL_PATH
)

sentiment_word_tfidf = joblib.load(
    SENTIMENT_WORD_TFIDF_PATH
)

sentiment_char_tfidf = joblib.load(
    SENTIMENT_CHAR_TFIDF_PATH
)

print("Sentiment model loaded successfully.")


# ============================================================
# SENTIMENT PREDICTION
# ============================================================

def predict_sentiment(text: str) -> str:
    """
    Predict sentiment using:
        Word TF-IDF
        +
        Character TF-IDF
        ↓
        LinearSVC sentiment model
    """

    # Word-level features
    word_features = sentiment_word_tfidf.transform(
        [text]
    )

    # Character-level features
    char_features = sentiment_char_tfidf.transform(
        [text]
    )

    # Combine both feature sets
    combined_features = hstack(
        [
            word_features,
            char_features
        ]
    )

    # Predict sentiment
    sentiment = sentiment_model.predict(
        combined_features
    )[0]

    return sentiment


# ============================================================
# TEXT CLEANING
# ============================================================

def clean_text(text: str) -> str:
    """
    Basic text cleaning.

    Keeps the original meaning while removing
    unnecessary whitespace.
    """

    if not isinstance(text, str):
        return ""

    # Replace multiple spaces/newlines with one space
    text = re.sub(
        r"\s+",
        " ",
        text
    )

    # Remove leading/trailing spaces
    text = text.strip()

    return text


# ============================================================
# ORDER ID EXTRACTION
# ============================================================

def extract_order_id(text: str):
    """
    Extract order ID from customer ticket.

    Supported examples:

        #12345
        ORD12345
        ORD-12345
        ORDER12345
        ORDER-12345
    """

    patterns = [

        # Example: #12345
        r"#(\d+)",

        # Example: ORD12345 / ORD-12345
        r"\bORD[- ]?(\d+)\b",

        # Example: ORDER12345 / ORDER-12345
        r"\bORDER[- ]?(\d+)\b"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            return match.group(1)

    return None


# ============================================================
# PRODUCT EXTRACTION
# ============================================================

def extract_product(text: str):
    """
    Basic product entity extraction.

    This is currently rule-based because we do not
    have a dedicated product NER model.

    Later this can be replaced with an NER model.
    """

    product_keywords = [

        "laptop",
        "phone",
        "mobile",
        "smartphone",

        "headphones",
        "earphones",
        "earbuds",

        "tablet",
        "watch",

        "shoes",
        "shirt",
        "dress",

        "camera",

        "television",
        "tv",

        "keyboard",
        "mouse",
        "charger",

        "bag",

        "refrigerator",
        "washing machine"
    ]

    text_lower = text.lower()

    found_products = []

    for product in product_keywords:

        pattern = (
            r"\b"
            + re.escape(product)
            + r"\b"
        )

        if re.search(
            pattern,
            text_lower
        ):
            found_products.append(product)

    # Remove duplicates while preserving order
    found_products = list(
        dict.fromkeys(found_products)
    )

    return found_products


# ============================================================
# INTENT EXTRACTION
# ============================================================

def extract_intent(text: str):
    """
    Extract customer intent using keyword-based rules.

    This is a temporary deterministic intent extractor.
    It can later be replaced by a trained intent model.
    """

    text_lower = text.lower()

    intent_rules = {

        "refund_request": [

            "refund",
            "money back",
            "want my money back"
        ],

        "return_request": [

            "return",
            "send it back",
            "return the product"
        ],

        "cancellation_request": [

            "cancel",
            "cancellation",
            "cancel my order"
        ],

        "delivery_issue": [

            "delivery",
            "delayed",
            "delay",
            "late delivery",
            "not delivered",
            "hasn't arrived",
            "has not arrived",
            "didn't arrive",
            "did not arrive"
        ],

        "damaged_product": [

            "damaged",
            "damage",
            "broken",
            "defective",
            "cracked",
            "not working"
        ],

        "payment_issue": [

            "payment failed",
            "payment issue",
            "payment problem",
            "payment",
            "charged"
        ],

        "replacement_request": [

            "replacement",
            "replace",
            "exchange"
        ],

        "order_tracking": [

            "track my order",
            "tracking",
            "tracking number",
            "track order"
        ]
    }

    for intent, keywords in intent_rules.items():

        for keyword in keywords:

            if keyword in text_lower:

                return intent

    return "general_query"


# ============================================================
# INTAKE AGENT
# ============================================================

class IntakeAgent:
    """
    Intake Agent

    Responsibilities:

    1. Clean ticket text
    2. Extract intent
    3. Predict sentiment
    4. Extract key entities
       - Order ID
       - Product
    5. Return structured ticket information
    """

    def __init__(self):

        self.name = "IntakeAgent"

    # --------------------------------------------------------
    # PROCESS TICKET
    # --------------------------------------------------------

    def process(
        self,
        ticket_text: str
    ) -> Dict[str, Any]:

        # ----------------------------------------------------
        # 1. VALIDATE INPUT
        # ----------------------------------------------------

        if not ticket_text:

            return {
                "status": "error",
                "error": "Ticket text is required.",
                "agent": self.name
            }

        if not isinstance(
            ticket_text,
            str
        ):

            return {
                "status": "error",
                "error": "Ticket must be a string.",
                "agent": self.name
            }

        # ----------------------------------------------------
        # 2. CLEAN TEXT
        # ----------------------------------------------------

        cleaned_text = clean_text(
            ticket_text
        )

        if not cleaned_text:

            return {
                "status": "error",
                "error": "Ticket is empty after cleaning.",
                "agent": self.name
            }

        # ----------------------------------------------------
        # 3. EXTRACT INTENT
        # ----------------------------------------------------

        intent = extract_intent(
            cleaned_text
        )

        # ----------------------------------------------------
        # 4. PREDICT SENTIMENT
        # ----------------------------------------------------

        sentiment = predict_sentiment(
            cleaned_text
        )

        # ----------------------------------------------------
        # 5. EXTRACT ORDER ID
        # ----------------------------------------------------

        order_id = extract_order_id(
            cleaned_text
        )

        # ----------------------------------------------------
        # 6. EXTRACT PRODUCT
        # ----------------------------------------------------

        product = extract_product(
            cleaned_text
        )

        # ----------------------------------------------------
        # 7. CREATE STRUCTURED OUTPUT
        # ----------------------------------------------------

        result = {

            "status": "success",

            "agent": self.name,

            "original_text": ticket_text,

            "cleaned_text": cleaned_text,

            "intent": intent,

            "sentiment": sentiment,

            "entities": {

                "order_id": order_id,

                "product": product
            },

            "intake_completed": True
        }

        return result


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    agent = IntakeAgent()

    test_ticket = (
        "My order #12345 arrived damaged. "
        "I want a replacement for my laptop."
    )

    result = agent.process(
        test_ticket
    )

    print("\n")
    print("=" * 60)
    print("INTAKE AGENT RESULT")
    print("=" * 60)

    for key, value in result.items():

        print(f"\n{key}: {value}")

    print("\n")
    print("=" * 60)