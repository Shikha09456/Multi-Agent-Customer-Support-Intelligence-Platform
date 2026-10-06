from pydantic import BaseModel, Field
from typing import Optional, Dict


class TicketRequest(BaseModel):
    ticket_id: str = Field(
        ...,
        description="Unique ticket ID"
    )

    ticket_text: str = Field(
        ...,
        min_length=1,
        description="Customer support ticket"
    )


class TicketResponse(BaseModel):
    ticket_id: str

    intent: Optional[str] = None
    sentiment: Optional[str] = None

    category: Optional[str] = None
    priority: Optional[str] = None

    classification_confidence: Optional[Dict[str, float]] = None

    customer_response: Optional[str] = None

    escalation_required: Optional[bool] = None
    escalation_level: Optional[str] = None
    escalation_reason: Optional[str] = None

    learning_status: Optional[str] = None
    database_id: Optional[int] = None
