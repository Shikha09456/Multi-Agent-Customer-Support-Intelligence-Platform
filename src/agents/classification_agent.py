from pathlib import Path
from typing import Dict, Any

import joblib


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

MODELS_DIR = PROJECT_ROOT / "models"


# ============================================================
# MODEL PATHS
# ============================================================

CATEGORY_MODEL_PATH = (
    MODELS_DIR / "ticket_category_model.pkl"
)

CATEGORY_TFIDF_PATH = (
    MODELS_DIR / "ticket_category_tfidf.pkl"
)

PRIORITY_MODEL_PATH = (
    MODELS_DIR / "priority_model.pkl"
)

PRIORITY_TFIDF_PATH = (
    MODELS_DIR / "priority_tfidf.pkl"
)


# ============================================================
# LOAD MODELS
# ============================================================

print("Loading classification models...")

category_model = joblib.load(
    CATEGORY_MODEL_PATH
)

category_tfidf = joblib.load(
    CATEGORY_TFIDF_PATH
)

priority_model = joblib.load(
    PRIORITY_MODEL_PATH
)

priority_tfidf = joblib.load(
    PRIORITY_TFIDF_PATH
)

print("Classification models loaded successfully.")


# ============================================================
# CATEGORY PREDICTION
# ============================================================

def predict_category(text: str):
    """
    Predict ticket category.
    """

    features = category_tfidf.transform(
        [text]
    )

    category = category_model.predict(
        features
    )[0]

    # Logistic Regression supports predict_proba
    if hasattr(category_model, "predict_proba"):

        probabilities = category_model.predict_proba(
            features
        )[0]

        confidence = float(
            probabilities.max()
        )

    else:
        confidence = None

    return category, confidence


# ============================================================
# PRIORITY PREDICTION
# ============================================================

def predict_priority(text: str):
    """
    Predict ticket priority.
    """

    features = priority_tfidf.transform(
        [text]
    )

    priority = priority_model.predict(
        features
    )[0]

    # Logistic Regression supports predict_proba
    if hasattr(priority_model, "predict_proba"):

        probabilities = priority_model.predict_proba(
            features
        )[0]

        confidence = float(
            probabilities.max()
        )

    else:
        confidence = None

    return priority, confidence


# ============================================================
# CLASSIFICATION AGENT
# ============================================================

class ClassificationAgent:
    """
    Classification Agent

    Responsibilities:

    1. Receive cleaned ticket text from Intake Agent
    2. Predict ticket category
    3. Predict ticket priority
    4. Return classification results
    """

    def __init__(self):

        self.name = "ClassificationAgent"

    # --------------------------------------------------------
    # PROCESS
    # --------------------------------------------------------

    def process(
        self,
        ticket_state: Dict[str, Any]
    ) -> Dict[str, Any]:

        # ----------------------------------------------------
        # Validate input
        # ----------------------------------------------------

        if not ticket_state:

            return {
                "status": "error",
                "error": "Ticket state is required.",
                "agent": self.name
            }

        # ----------------------------------------------------
        # Get cleaned text
        # ----------------------------------------------------

        text = ticket_state.get(
            "cleaned_text"
        )

        if not text:

            return {
                "status": "error",
                "error": "cleaned_text is missing.",
                "agent": self.name
            }

        # ----------------------------------------------------
        # Predict category
        # ----------------------------------------------------

        category, category_confidence = (
            predict_category(text)
        )

        # ----------------------------------------------------
        # Predict priority
        # ----------------------------------------------------

        priority, priority_confidence = (
            predict_priority(text)
        )

        # ----------------------------------------------------
        # Update existing state
        # ----------------------------------------------------

        ticket_state["category"] = category

        ticket_state["priority"] = priority

        ticket_state["classification_confidence"] = {

            "category": category_confidence,

            "priority": priority_confidence
        }

        ticket_state[
            "classification_completed"
        ] = True

        ticket_state["classification_agent"] = (
            self.name
        )

        return ticket_state


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    agent = ClassificationAgent()

    # This simulates the output received
    # from the Intake Agent.

    test_ticket_state = {

        "status": "success",

        "agent": "IntakeAgent",

        "original_text":
            "My order #12345 arrived damaged. "
            "I want a replacement for my laptop.",

        "cleaned_text":
            "My order #12345 arrived damaged. "
            "I want a replacement for my laptop.",

        "intent":
            "damaged_product",

        "sentiment":
            "Negative",

        "entities": {

            "order_id": "12345",

            "product": ["laptop"]
        },

        "intake_completed": True
    }

    result = agent.process(
        test_ticket_state
    )

    print("\n")
    print("=" * 60)
    print("CLASSIFICATION AGENT RESULT")
    print("=" * 60)

    for key, value in result.items():

        print(f"\n{key}: {value}")

    print("\n")
    print("=" * 60)
