from typing import Dict, Any


# ============================================================
# ESCALATION AGENT
# ============================================================

class EscalationAgent:
    """
    Escalation Agent

    Responsibilities:
    1. Analyze ticket priority
    2. Analyze customer sentiment
    3. Analyze classification confidence
    4. Check whether the ticket should be escalated
    5. Provide an escalation reason
    """

    def __init__(self):

        self.name = "EscalationAgent"

    # ========================================================
    # ESCALATION DECISION
    # ========================================================

    def evaluate(
        self,
        ticket_state: Dict[str, Any]
    ) -> Dict[str, Any]:

        reasons = []

        # ----------------------------------------------------
        # Get information from previous agents
        # ----------------------------------------------------

        priority = str(
            ticket_state.get(
                "priority",
                ""
            )
        ).lower()

        sentiment = str(
            ticket_state.get(
                "sentiment",
                ""
            )
        ).lower()

        confidence = ticket_state.get(
            "classification_confidence",
            {}
        )

        category_confidence = confidence.get(
            "category"
        )

        priority_confidence = confidence.get(
            "priority"
        )

        # ----------------------------------------------------
        # Rule 1: High / Critical Priority
        # ----------------------------------------------------

        high_priority_values = [
            "high",
            "critical",
            "urgent"
        ]

        if priority in high_priority_values:

            reasons.append(
                f"Ticket priority is {priority}."
            )

        # ----------------------------------------------------
        # Rule 2: Very negative sentiment
        # ----------------------------------------------------

        negative_sentiments = [
            "very negative",
            "negative"
        ]

        if sentiment in negative_sentiments:

            reasons.append(
                f"Customer sentiment is {sentiment}."
            )

        # ----------------------------------------------------
        # Rule 3: Low classification confidence
        # ----------------------------------------------------

        confidence_threshold = 0.60

        if (
            category_confidence is not None
            and
            category_confidence < confidence_threshold
        ):

            reasons.append(
                "Ticket category classification "
                "has low confidence."
            )

        if (
            priority_confidence is not None
            and
            priority_confidence < confidence_threshold
        ):

            reasons.append(
                "Ticket priority classification "
                "has low confidence."
            )

        # ----------------------------------------------------
        # Rule 4: No relevant FAQ
        # ----------------------------------------------------

        retrieved_documents = ticket_state.get(
            "retrieved_documents",
            []
        )

        if not retrieved_documents:

            reasons.append(
                "No relevant knowledge-base information "
                "was retrieved."
            )

        # ----------------------------------------------------
        # Rule 5: Very low retrieval similarity
        # ----------------------------------------------------

        if retrieved_documents:

            top_score = retrieved_documents[0].get(
                "score",
                0
            )

            retrieval_threshold = 0.35

            if top_score < retrieval_threshold:

                reasons.append(
                    "Retrieved knowledge-base results "
                    "have low similarity."
                )

        # ----------------------------------------------------
        # FINAL DECISION
        # ----------------------------------------------------

        escalation_required = len(reasons) > 0

        # ----------------------------------------------------
        # Escalation Level
        # ----------------------------------------------------

        if priority == "critical":

            escalation_level = "critical"

        elif priority in [
            "high",
            "urgent"
        ]:

            escalation_level = "high"

        elif escalation_required:

            escalation_level = "medium"

        else:

            escalation_level = "none"

        # ----------------------------------------------------
        # Escalation Reason
        # ----------------------------------------------------

        if escalation_required:

            escalation_reason = "; ".join(
                reasons
            )

        else:

            escalation_reason = (
                "Ticket can be handled automatically."
            )

        return {

            "escalation_required":
                escalation_required,

            "escalation_level":
                escalation_level,

            "escalation_reason":
                escalation_reason,

            "escalation_completed":
                True
        }

    # ========================================================
    # PROCESS
    # ========================================================

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

                "error":
                    "Ticket state is required.",

                "agent":
                    self.name
            }

        # ----------------------------------------------------
        # Evaluate escalation
        # ----------------------------------------------------

        escalation_result = self.evaluate(
            ticket_state
        )

        # ----------------------------------------------------
        # Add results to shared state
        # ----------------------------------------------------

        ticket_state.update(
            escalation_result
        )

        ticket_state[
            "escalation_agent"
        ] = self.name

        return ticket_state


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    agent = EscalationAgent()

    # Simulated state after:
    # Intake → Classification → Retrieval → Response

    test_ticket_state = {

        "status": "success",

        "cleaned_text":
            "My order #12345 arrived damaged. "
            "I want a replacement for my laptop.",

        "intent":
            "damaged_product",

        "sentiment":
            "Very Negative",

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

        "classification_confidence": {

            "category":
                0.82,

            "priority":
                0.91
        },

        "retrieved_documents": [

            {

                "faq_id":
                    "FAQ_001",

                "score":
                    0.81,

                "category":
                    "Damaged Product",

                "text":
                    "Customers can request "
                    "a replacement for damaged products."
            }
        ],

        "customer_response":
            "We're sorry that your product arrived damaged."
    }

    # --------------------------------------------------------
    # Run agent
    # --------------------------------------------------------

    result = agent.process(
        test_ticket_state
    )

    # --------------------------------------------------------
    # Display result
    # --------------------------------------------------------

    print("\n")
    print("=" * 70)
    print("ESCALATION AGENT RESULT")
    print("=" * 70)

    print(
        "\nEscalation Required:",
        result.get(
            "escalation_required"
        )
    )

    print(
        "\nEscalation Level:",
        result.get(
            "escalation_level"
        )
    )

    print(
        "\nEscalation Reason:",
        result.get(
            "escalation_reason"
        )
    )

    print(
        "\nEscalation Completed:",
        result.get(
            "escalation_completed"
        )
    )

    print("\n")
    print("=" * 70)