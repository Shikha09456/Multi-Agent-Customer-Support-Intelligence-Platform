from src.agents.response_agent import ResponseAgent


agent = ResponseAgent()

state = {
    "cleaned_text": "My order has not arrived yet. Please help me track it.",
    "intent": "delivery_issue",
    "sentiment": "Negative",
    "category": "Delivery Issue",
    "priority": "High",

    "entities": {
        "order_id": None,
        "product": None
    },

    "retrieved_documents": [
        {
            "score": 0.85,
            "faq_id": 1,
            "category": "Delivery Issue",
            "text": "Customers can track their order using the tracking link provided after shipment."
        }
    ],

    "retrieval_completed": True
}


result = agent.process(state)

print("\n" + "=" * 60)
print("RESPONSE AGENT TEST")
print("=" * 60)

print("\nCustomer Response:")
print(result.get("customer_response"))

print("\nResponse Generated:")
print(result.get("response_generated"))

print("\nResponse Agent:")
print(result.get("response_agent"))