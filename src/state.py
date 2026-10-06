from typing import TypedDict, List, Dict, Any, Optional


class TicketState(TypedDict, total=False):

    # =========================
    # Ticket / Intake
    # =========================

    ticket_id: str
    original_text: str
    cleaned_text: str

    intent: str
    sentiment: str

    entities: Dict[str, Any]

    intake_completed: bool
    intake_agent: str

    # =========================
    # Classification
    # =========================

    category: str
    priority: str

    classification_confidence: Dict[str, float]

    classification_completed: bool
    classification_agent: str

    # =========================
    # Retrieval
    # =========================

    retrieved_documents: List[Dict[str, Any]]

    retrieval_completed: bool
    retrieval_agent: str

    # =========================
    # Response
    # =========================

    customer_response: str

    response_generated: bool
    response_agent: str

    # =========================
    # Escalation
    # =========================

    escalation_required: bool
    escalation_level: str
    escalation_reason: str

    escalation_completed: bool
    escalation_agent: str

    # =========================
    # Learning / Database
    # =========================

    resolution_text: Optional[str]

    customer_satisfaction_score: Optional[float]

    retrieval_feedback: Optional[str]
    human_feedback: Optional[str]

    prompt_strategy: Optional[str]
    prompt_version: Optional[str]

    learning_completed: bool
    learning_agent: str

    learning_status: str
    database_id: Optional[int]
    learning_error: Optional[str]
