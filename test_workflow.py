from src.workflow.workflow import workflow


# ============================================================
# TEST TICKET
# ============================================================

ticket = {
    "ticket_id": "WORKFLOW_TEST_001",

    "original_text":
        "My order has not arrived yet. Please help me track it.",

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


# ============================================================
# RUN LANGGRAPH WORKFLOW
# ============================================================

result = workflow.invoke(ticket)


# ============================================================
# DISPLAY RESULT
# ============================================================

print("\n" + "=" * 60)
print("WORKFLOW COMPLETED")
print("=" * 60)

print("\nTicket ID:")
print(result.get("ticket_id"))

print("\nIntent:")
print(result.get("intent"))

print("\nSentiment:")
print(result.get("sentiment"))

print("\nCategory:")
print(result.get("category"))

print("\nPriority:")
print(result.get("priority"))

print("\nClassification Confidence:")
print(result.get("classification_confidence"))

print("\nEscalation Required:")
print(result.get("escalation_required"))

print("\nEscalation Level:")
print(result.get("escalation_level"))

print("\nEscalation Reason:")
print(result.get("escalation_reason"))

print("\nCustomer Response:")
print(result.get("customer_response"))

print("\nLearning Status:")
print(result.get("learning_status"))

print("\nDatabase ID:")
print(result.get("database_id"))

print("\n" + "=" * 60)

result = workflow.invoke(ticket)

print("\nRetrieved Documents:")
for doc in result.get("retrieved_documents", []):
    print(
        f"FAQ ID: {doc.get('faq_id')} | "
        f"Score: {doc.get('score')}"
    )

print("\nResponse Generated:")
print(result.get("response_generated"))

print("\nResponse Agent:")
print(result.get("response_agent"))