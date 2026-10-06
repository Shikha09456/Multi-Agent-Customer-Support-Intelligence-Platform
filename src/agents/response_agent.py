from typing import Dict, Any
import requests


# ============================================================
# OLLAMA CONFIGURATION
# ============================================================

OLLAMA_URL = "http://localhost:11434/api/generate"

# Agar tumhare system me model ka naam different hai,
# ise apne installed Ollama model ke naam se change karna.
OLLAMA_MODEL = "gemma3:4b"


# ============================================================
# RESPONSE AGENT
# ============================================================

class ResponseAgent:
    """
    Response Agent

    Responsibilities:
    1. Receive complete ticket state
    2. Use ticket information
    3. Use retrieved FAQ knowledge
    4. Generate a customer-friendly response using LLM
    """

    def __init__(
        self,
        model: str = OLLAMA_MODEL,
        ollama_url: str = OLLAMA_URL
    ):

        self.name = "ResponseAgent"

        self.model = model

        self.ollama_url = ollama_url


    # ========================================================
    # BUILD CONTEXT
    # ========================================================

    def build_context(
        self,
        ticket_state: Dict[str, Any]
    ) -> str:

        context_parts = []

        # ----------------------------------------------------
        # Ticket information
        # ----------------------------------------------------

        context_parts.append(
            f"Customer Ticket:\n"
            f"{ticket_state.get('cleaned_text', '')}"
        )

        # ----------------------------------------------------
        # Intent
        # ----------------------------------------------------

        context_parts.append(
            f"Intent:\n"
            f"{ticket_state.get('intent', 'Unknown')}"
        )

        # ----------------------------------------------------
        # Sentiment
        # ----------------------------------------------------

        context_parts.append(
            f"Customer Sentiment:\n"
            f"{ticket_state.get('sentiment', 'Unknown')}"
        )

        # ----------------------------------------------------
        # Category
        # ----------------------------------------------------

        context_parts.append(
            f"Ticket Category:\n"
            f"{ticket_state.get('category', 'Unknown')}"
        )

        # ----------------------------------------------------
        # Priority
        # ----------------------------------------------------

        context_parts.append(
            f"Ticket Priority:\n"
            f"{ticket_state.get('priority', 'Unknown')}"
        )

        # ----------------------------------------------------
        # Entities
        # ----------------------------------------------------

        entities = ticket_state.get(
            "entities",
            {}
        )

        context_parts.append(
            f"Order ID:\n"
            f"{entities.get('order_id', 'Not provided')}"
        )

        context_parts.append(
            f"Product:\n"
            f"{entities.get('product', 'Not provided')}"
        )

        # ----------------------------------------------------
        # Retrieved FAQ documents
        # ----------------------------------------------------

        retrieved_documents = ticket_state.get(
            "retrieved_documents",
            []
        )

        faq_context = []

        for i, document in enumerate(
            retrieved_documents,
            start=1
        ):

            faq_text = document.get(
                "text",
                ""
            )

            faq_category = document.get(
                "category",
                ""
            )

            faq_score = document.get(
                "score",
                0
            )

            faq_context.append(
                f"""
FAQ {i}
Category: {faq_category}
Similarity Score: {faq_score:.4f}

{faq_text}
"""
            )

        if faq_context:

            context_parts.append(
                "Relevant Knowledge Base Information:\n"
                + "\n".join(faq_context)
            )

        else:

            context_parts.append(
                "Relevant Knowledge Base Information:\n"
                "No relevant FAQ was retrieved."
            )

        return "\n\n".join(
            context_parts
        )


    # ========================================================
    # CREATE PROMPT
    # ========================================================

    def build_prompt(
        self,
        ticket_state: Dict[str, Any]
    ) -> str:

        context = self.build_context(
            ticket_state
        )

        prompt = f"""
You are a professional e-commerce customer support assistant.

Your job is to respond to the customer using the
provided ticket information and knowledge base.

IMPORTANT RULES:

1. Use the provided knowledge base information.
2. Do not invent policies, refunds, delivery dates,
   compensation, or procedures.
3. If the knowledge base does not contain enough
   information, clearly say that the issue needs
   further assistance.
4. Be polite, concise, and professional.
5. Do not mention that you are an AI.
6. Do not expose internal classification details.
7. Do not mention similarity scores.
8. Do not make up an order status.
9. Address the customer's actual issue directly.
10. If the customer is upset, respond empathetically.

TICKET INFORMATION
==================

{context}


RESPONSE REQUIREMENTS
=====================

Write only the final customer-facing response.

The response should:

- acknowledge the customer's issue
- provide the relevant solution/information
- mention the order ID if available and useful
- be clear and professional
- avoid unnecessary technical details
"""

        return prompt


    # ========================================================
    # CALL OLLAMA
    # ========================================================

    def generate_response(
        self,
        prompt: str
    ) -> str:

        payload = {

            "model": self.model,

            "prompt": prompt,

            "stream": False,

            "options": {

                "temperature": 0.2
            }
        }

        try:

            response = requests.post(
                self.ollama_url,
                json=payload,
                timeout=120
            )

            response.raise_for_status()

            result = response.json()

            generated_text = result.get(
                "response",
                ""
            ).strip()

            if not generated_text:

                return (
                    "I’m sorry, but I’m unable to "
                    "generate a response right now."
                )

            return generated_text

        except requests.exceptions.ConnectionError:

            return (
                "I’m sorry, but the customer support "
                "service is temporarily unavailable. "
                "Please try again shortly."
            )

        except requests.exceptions.Timeout:

            return (
                "I’m sorry, but the response is taking "
                "longer than expected. Please try again."
            )

        except requests.exceptions.RequestException as e:

            print(
                f"Ollama API error: {e}"
            )

            return (
                "I’m sorry, but I’m unable to process "
                "your request right now."
            )


    # ========================================================
    # PROCESS
    # ========================================================

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
        # Check retrieval
        # ----------------------------------------------------

        if not ticket_state.get(
            "retrieval_completed",
            False
        ):

            return {

                "status": "error",

                "error":
                    "Retrieval Agent must run before "
                    "Response Agent.",

                "agent":
                    self.name
            }


        # ----------------------------------------------------
        # Build prompt
        # ----------------------------------------------------

        prompt = self.build_prompt(
            ticket_state
        )


        # ----------------------------------------------------
        # Generate response
        # ----------------------------------------------------

        customer_response = self.generate_response(
            prompt
        )


        # ----------------------------------------------------
        # Update state
        # ----------------------------------------------------

        ticket_state[
            "customer_response"
        ] = customer_response

        ticket_state[
            "response_generated"
        ] = True

        ticket_state[
            "response_agent"
        ] = self.name


        return ticket_state


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    agent = ResponseAgent()


    # Simulated output from previous agents

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
            True,

        "retrieved_documents": [

            {
                "faq_id":
                    "FAQ_001",

                "score":
                    0.82,

                "category":
                    "Damaged Product",

                "text":
                    "If a product arrives damaged, "
                    "customers can request a replacement "
                    "through the return and replacement "
                    "process."
            },

            {
                "faq_id":
                    "FAQ_002",

                "score":
                    0.74,

                "category":
                    "Returns",

                "text":
                    "Customers should provide their "
                    "order details when requesting "
                    "a replacement."
            }
        ],

        "retrieval_completed":
            True
    }


    # --------------------------------------------------------
    # Run Response Agent
    # --------------------------------------------------------

    result = agent.process(
        test_ticket_state
    )


    # --------------------------------------------------------
    # Display result
    # --------------------------------------------------------

    print("\n")
    print("=" * 70)
    print("RESPONSE AGENT RESULT")
    print("=" * 70)

    print("\nCustomer Response:")

    print(
        result.get(
            "customer_response",
            ""
        )
    )

    print("\n")
    print("=" * 70)
