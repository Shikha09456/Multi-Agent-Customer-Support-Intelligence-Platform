import json
from datetime import datetime

from src.database import get_connection


def learning_agent(ticket_state):
    """
    Learning Agent

    Responsibilities:
    1. Store complete ticket -> response -> resolution mapping
    2. Store retrieved documents for retrieval analysis
    3. Store escalation decisions
    4. Store customer satisfaction
    5. Store human/retrieval feedback
    6. Store prompt version for future prompt evaluation
    """

    try:
        # ---------------------------------------------------------
        # Extract values from workflow state
        # ---------------------------------------------------------

        ticket_id = ticket_state.get("ticket_id")

        ticket_text = ticket_state.get(
            "original_text",
            ticket_state.get("ticket_text", "")
        )

        cleaned_text = ticket_state.get("cleaned_text", "")

        intent = ticket_state.get("intent")

        sentiment = ticket_state.get("sentiment")

        category = ticket_state.get("category")

        priority = ticket_state.get("priority")

        # ---------------------------------------------------------
        # Entities
        # ---------------------------------------------------------

        entities = ticket_state.get("entities", {})

        order_id = entities.get("order_id")

        product = entities.get("product", [])

        if isinstance(product, list):
            product = ", ".join(product)

        # ---------------------------------------------------------
        # Retrieved documents
        # ---------------------------------------------------------

        retrieved_documents = ticket_state.get(
            "retrieved_documents",
            []
        )

        # JSONB column ke liye Python list ko JSON string me convert
        retrieved_documents_json = json.dumps(
            retrieved_documents,
            default=str
        )

        # ---------------------------------------------------------
        # Customer response
        # ---------------------------------------------------------

        customer_response = ticket_state.get(
            "customer_response",
            ""
        )

        # ---------------------------------------------------------
        # Escalation information
        # ---------------------------------------------------------

        escalation_required = ticket_state.get(
            "escalation_required",
            False
        )

        escalation_level = ticket_state.get(
            "escalation_level"
        )

        escalation_reason = ticket_state.get(
            "escalation_reason"
        )

        # ---------------------------------------------------------
        # Resolution information
        # ---------------------------------------------------------

        resolution_text = ticket_state.get(
            "resolution_text"
        )

        customer_satisfaction_score = ticket_state.get(
            "customer_satisfaction_score"
        )

        # ---------------------------------------------------------
        # Feedback
        # ---------------------------------------------------------

        retrieval_feedback = ticket_state.get(
            "retrieval_feedback"
        )

        human_feedback = ticket_state.get(
            "human_feedback"
        )

        # ---------------------------------------------------------
        # Prompt information
        # ---------------------------------------------------------

        prompt_strategy = ticket_state.get(
            "prompt_strategy",
            "faq_grounded_response"
        )

        prompt_version = ticket_state.get(
            "prompt_version",
            "v1"
        )

        # ---------------------------------------------------------
        # Database connection
        # ---------------------------------------------------------

        connection = get_connection()

        cursor = connection.cursor()

        # ---------------------------------------------------------
        # Insert interaction into PostgreSQL
        # ---------------------------------------------------------

        query = """
        INSERT INTO support_interactions (
            ticket_id,
            ticket_text,
            cleaned_text,
            intent,
            sentiment,
            category,
            priority,
            order_id,
            product,
            retrieved_documents,
            customer_response,
            escalation_required,
            escalation_level,
            escalation_reason,
            resolution_text,
            customer_satisfaction_score,
            retrieval_feedback,
            human_feedback,
            prompt_strategy,
            prompt_version,
            created_at,
            resolved_at
        )
        VALUES (
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s::jsonb,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s
        )
        RETURNING id;
        """

        values = (
            ticket_id,
            ticket_text,
            cleaned_text,
            intent,
            sentiment,
            category,
            priority,
            order_id,
            product,
            retrieved_documents_json,
            customer_response,
            escalation_required,
            escalation_level,
            escalation_reason,
            resolution_text,
            customer_satisfaction_score,
            retrieval_feedback,
            human_feedback,
            prompt_strategy,
            prompt_version,
            datetime.now(),
            datetime.now() if resolution_text else None
        )

        cursor.execute(query, values)

        database_id = cursor.fetchone()[0]

        connection.commit()

        cursor.close()
        connection.close()

        # ---------------------------------------------------------
        # Update workflow state
        # ---------------------------------------------------------

        ticket_state["learning_completed"] = True

        ticket_state["learning_agent"] = "LearningAgent"

        ticket_state["database_id"] = database_id

        ticket_state["learning_status"] = "saved"

        return ticket_state

    except Exception as e:

        print("Learning Agent Error:")
        print(e)

        ticket_state["learning_completed"] = False

        ticket_state["learning_agent"] = "LearningAgent"

        ticket_state["learning_status"] = "failed"

        ticket_state["learning_error"] = str(e)

        return ticket_state