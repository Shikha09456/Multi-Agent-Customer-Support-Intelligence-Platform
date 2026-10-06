from src.agents.learning_agent import learning_agent


test_state = {
    "ticket_id": "TEST001",

    "original_text": "My order has not arrived yet. Please help me.",

    "cleaned_text": "my order has not arrived yet please help me",

    "intent": "delivery_issue",

    "sentiment": "Negative",

    "category": "Delivery",

    "priority": "High",

    "entities": {
        "order_id": "ORD12345",
        "product": ["order"]
    },

    "retrieved_documents": [
        {
            "faq_id": "FAQ001",
            "score": 0.82,
            "text": "Customers can track their order using the tracking page."
        }
    ],

    "customer_response":
        "Please use the order tracking page to check the latest status of your order.",

    "escalation_required": True,

    "escalation_level": "high",

    "escalation_reason": "High priority ticket",

    "resolution_text":
        "Customer was provided with order tracking instructions.",

    "customer_satisfaction_score": 4,

    "retrieval_feedback": "useful",

    "human_feedback": "Response was relevant.",

    "prompt_strategy": "faq_grounded_response",

    "prompt_version": "v1"
}


result = learning_agent(test_state)

print("\n========== LEARNING AGENT RESULT ==========")

print("Learning completed:",
      result.get("learning_completed"))

print("Learning status:",
      result.get("learning_status"))

print("Database ID:",
      result.get("database_id"))

if result.get("learning_error"):
    print("Error:",
          result.get("learning_error"))