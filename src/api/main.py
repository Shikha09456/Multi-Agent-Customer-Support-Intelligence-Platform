from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List

from src.workflow.workflow import workflow


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="Multi-Agent Customer Support Intelligence Platform",
    description="Agentic customer support system using LangGraph, RAG and Ollama",
    version="1.0.0"
)


# ============================================================
# REQUEST SCHEMA
# ============================================================

class TicketRequest(BaseModel):
    ticket_id: str = Field(..., description="Unique ticket ID")
    ticket_text: str = Field(..., min_length=1, description="Customer support ticket")


# ============================================================
# RESPONSE SCHEMA
# ============================================================

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


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/")
def root():
    return {
        "status": "running",
        "message": "Multi-Agent Customer Support Intelligence Platform API"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# ============================================================
# PROCESS TICKET
# ============================================================

@app.post("/tickets", response_model=TicketResponse)
def process_ticket(ticket: TicketRequest):

    try:

        # ----------------------------------------------------
        # Initial LangGraph State
        # ----------------------------------------------------

        initial_state = {
            "ticket_id": ticket.ticket_id,
            "original_text": ticket.ticket_text,

            "cleaned_text": "",
            "entities": {},

            "retrieved_documents": [],

            "customer_response": "",

            "resolution_text": None,
            "customer_satisfaction_score": None,
            "retrieval_feedback": None,
            "human_feedback": None,

            "prompt_strategy": "faq_grounded_response",
            "prompt_version": "v1"
        }

        # ----------------------------------------------------
        # Execute LangGraph Workflow
        # ----------------------------------------------------

        result = workflow.invoke(initial_state)

        # ----------------------------------------------------
        # Return Final Result
        # ----------------------------------------------------

        return TicketResponse(
            ticket_id=result.get("ticket_id", ticket.ticket_id),

            intent=result.get("intent"),
            sentiment=result.get("sentiment"),

            category=result.get("category"),
            priority=result.get("priority"),

            classification_confidence=result.get(
                "classification_confidence"
            ),

            customer_response=result.get(
                "customer_response"
            ),

            escalation_required=result.get(
                "escalation_required"
            ),

            escalation_level=result.get(
                "escalation_level"
            ),

            escalation_reason=result.get(
                "escalation_reason"
            ),

            learning_status=result.get(
                "learning_status"
            ),

            database_id=result.get(
                "database_id"
            )
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
