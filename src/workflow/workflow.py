from langgraph.graph import StateGraph, START, END

from src.state import TicketState

from src.agents.intake_agent import IntakeAgent
from src.agents.classification_agent import ClassificationAgent
from src.agents.retrieval_agent import RetrievalAgent
from src.agents.response_agent import ResponseAgent
from src.agents.escalation_agent import EscalationAgent
from src.agents.learning_agent import learning_agent


# ============================================================
# AGENT INSTANCES
# ============================================================

intake = IntakeAgent()
classification = ClassificationAgent()
retrieval = RetrievalAgent(top_k=5)
response = ResponseAgent()
escalation = EscalationAgent()


# ============================================================
# NODE FUNCTIONS
# ============================================================

def intake_node(state: TicketState):
    """
    Intake Agent:
    - Cleans ticket
    - Detects intent
    - Detects sentiment
    - Extracts entities
    """
    return intake.process(
        state.get("original_text", "")
    )


def classification_node(state: TicketState):
    """
    Classification Agent:
    - Predicts category
    - Predicts priority
    - Calculates confidence
    """
    return classification.process(state)


def retrieval_node(state: TicketState):
    """
    Retrieval Agent:
    - Searches FAISS knowledge base
    - Retrieves relevant FAQ documents
    """
    return retrieval.process(state)


def response_node(state: TicketState):
    """
    Response Agent:
    - Uses retrieved knowledge
    - Generates grounded customer response
    """
    return response.process(state)


def escalation_node(state: TicketState):
    """
    Escalation Agent:
    - Checks priority
    - Checks sentiment
    - Checks classification confidence
    - Checks retrieval quality
    - Decides whether escalation is required
    """
    return escalation.process(state)


def learning_node(state: TicketState):
    """
    Learning Agent:
    - Stores interaction
    - Stores response
    - Stores escalation information
    - Stores feedback/learning information
    """
    return learning_agent(state)


# ============================================================
# CONDITIONAL ROUTER
# ============================================================

def route_after_classification(state: TicketState):
    """
    Decide what should happen after classification.

    Low-confidence classification:
        -> Escalation
        -> Learning
        -> END

    Sufficient-confidence classification:
        -> Retrieval
        -> Response
        -> Escalation
        -> Learning
        -> END
    """

    confidence = state.get(
        "classification_confidence",
        {}
    )

    category_conf = confidence.get("category")
    priority_conf = confidence.get("priority")

    # If confidence information is missing,
    # send the ticket for human review.
    if category_conf is None or priority_conf is None:
        return "escalation"

    # Low category confidence
    if category_conf < 0.60:
        return "escalation"

    # Low priority confidence
    if priority_conf < 0.60:
        return "escalation"

    # Classification is sufficiently confident
    return "retrieval"


# ============================================================
# BUILD LANGGRAPH
# ============================================================

graph = StateGraph(TicketState)


# ------------------------------------------------------------
# ADD NODES
# ------------------------------------------------------------

graph.add_node("intake", intake_node)
graph.add_node("classification", classification_node)
graph.add_node("retrieval", retrieval_node)
graph.add_node("response", response_node)
graph.add_node("escalation", escalation_node)
graph.add_node("learning", learning_node)


# ============================================================
# AGENT WORKFLOW
# ============================================================

graph.add_edge(START, "intake")
graph.add_edge("intake", "classification")
graph.add_edge("classification", "retrieval")
graph.add_edge("retrieval", "response")
graph.add_edge("response", "escalation")
graph.add_edge("escalation", "learning")
graph.add_edge("learning", END)


# ============================================================
# COMPILE WORKFLOW
# ============================================================

workflow = graph.compile()