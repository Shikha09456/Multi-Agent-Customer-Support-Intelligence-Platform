import streamlit as st
import requests
import time


# ============================================================
# CONFIGURATION
# ============================================================

API_URL = "http://127.0.0.1:8000"


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Customer Support",
    page_icon="🤖",
    layout="wide"
)


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "ticket_counter" not in st.session_state:
    st.session_state.ticket_counter = 1


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 32px;
        font-weight: 700;
    }

    .subtitle {
        color: #777;
        font-size: 16px;
        margin-bottom: 25px;
    }

    .response-box {
        padding: 18px;
        border-radius: 10px;
        border: 1px solid #ddd;
        margin-top: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">'
    '🤖 AI Customer Support Agent'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Multi-Agent Customer Support Intelligence Platform'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("⚙️ System Status")

    try:

        health_response = requests.get(
            f"{API_URL}/health",
            timeout=5
        )

        if health_response.status_code == 200:
            st.success("🟢 Backend Online")
        else:
            st.error("🔴 Backend Error")

    except requests.exceptions.RequestException:

        st.error("🔴 Backend Offline")

        st.caption(
            "Start FastAPI with:"
        )

        st.code(
            "uvicorn src.api.main:app --reload"
        )

    st.divider()

    st.subheader("🤖 Agents")

    st.write("🧾 Intake Agent")
    st.write("🧠 Classification Agent")
    st.write("📚 Retrieval Agent")
    st.write("✍️ Response Agent")
    st.write("🚨 Escalation Agent")
    st.write("📊 Learning Agent")

    st.divider()

    if st.button(
        "🗑️ Clear Chat",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.rerun()


# ============================================================
# DISPLAY CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )

        if message["role"] == "assistant":

            result = message.get(
                "result"
            )

            if result:

                with st.expander(
                    "🔍 Agent Logs"
                ):

                    # ----------------------------------------
                    # INTAKE
                    # ----------------------------------------

                    st.markdown(
                        "### 🧾 Intake Agent"
                    )

                    st.write(
                        f"**Intent:** "
                        f"{result.get('intent', 'N/A')}"
                    )

                    st.write(
                        f"**Sentiment:** "
                        f"{result.get('sentiment', 'N/A')}"
                    )

                    # ----------------------------------------
                    # CLASSIFICATION
                    # ----------------------------------------

                    st.markdown(
                        "### 🧠 Classification Agent"
                    )

                    st.write(
                        f"**Category:** "
                        f"{result.get('category', 'N/A')}"
                    )

                    st.write(
                        f"**Priority:** "
                        f"{result.get('priority', 'N/A')}"
                    )

                    # ----------------------------------------
                    # CONFIDENCE
                    # ----------------------------------------

                    st.markdown(
                        "### 📊 Confidence"
                    )

                    confidence = result.get(
                        "classification_confidence",
                        {}
                    )

                    if confidence:

                        category_conf = float(
                            confidence.get(
                                "category",
                                0
                            )
                        )

                        priority_conf = float(
                            confidence.get(
                                "priority",
                                0
                            )
                        )

                        st.write(
                            f"Category: "
                            f"{category_conf * 100:.2f}%"
                        )

                        st.progress(
                            min(
                                category_conf,
                                1.0
                            )
                        )

                        st.write(
                            f"Priority: "
                            f"{priority_conf * 100:.2f}%"
                        )

                        st.progress(
                            min(
                                priority_conf,
                                1.0
                            )
                        )

                    # ----------------------------------------
                    # RETRIEVAL
                    # ----------------------------------------

                    st.markdown(
                        "### 📚 Retrieval Agent"
                    )

                    retrieved = result.get(
                        "retrieved_documents",
                        []
                    )

                    if retrieved:

                        for doc in retrieved:

                            st.write(
                                f"• "
                                f"{doc.get('faq_id', 'N/A')} "
                                f"| Score: "
                                f"{doc.get('score', 0):.3f}"
                            )

                    else:

                        st.write(
                            "No documents retrieved."
                        )

                    # ----------------------------------------
                    # RESPONSE
                    # ----------------------------------------

                    st.markdown(
                        "### ✍️ Response Agent"
                    )

                    st.write(
                        "Model: Ollama / Gemma 3"
                    )

                    st.write(
                        f"Generated: "
                        f"{result.get('response_generated', False)}"
                    )

                    # ----------------------------------------
                    # ESCALATION
                    # ----------------------------------------

                    st.markdown(
                        "### 🚨 Escalation Agent"
                    )

                    st.write(
                        f"Required: "
                        f"{result.get('escalation_required', False)}"
                    )

                    st.write(
                        f"Level: "
                        f"{result.get('escalation_level', 'N/A')}"
                    )

                    reason = result.get(
                        "escalation_reason"
                    )

                    if reason:

                        st.write(
                            f"Reason: {reason}"
                        )

                    # ----------------------------------------
                    # LEARNING
                    # ----------------------------------------

                    st.markdown(
                        "### 📊 Learning Agent"
                    )

                    st.write(
                        f"Status: "
                        f"{result.get('learning_status', 'N/A')}"
                    )

                    st.write(
                        f"Database ID: "
                        f"{result.get('database_id', 'N/A')}"
                    )


# ============================================================
# CHAT INPUT
# ============================================================

prompt = st.chat_input(
    "Describe your issue..."
)


# ============================================================
# PROCESS NEW TICKET
# ============================================================

if prompt:

    ticket_id = (
        f"CHAT_"
        f"{st.session_state.ticket_counter:03d}"
    )

    st.session_state.ticket_counter += 1

    # --------------------------------------------------------
    # USER MESSAGE
    # --------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):

        st.markdown(prompt)

    # --------------------------------------------------------
    # ASSISTANT
    # --------------------------------------------------------

    with st.chat_message("assistant"):

        status = st.empty()

        try:

            # ----------------------------------------------
            # PROCESSING SIMULATION
            # ----------------------------------------------

            status.info(
                "🧾 Intake Agent analyzing ticket..."
            )

            time.sleep(0.5)

            status.info(
                "🧠 Classification Agent analyzing ticket..."
            )

            time.sleep(0.5)

            status.info(
                "📚 Retrieval Agent searching knowledge base..."
            )

            time.sleep(0.5)

            # ----------------------------------------------
            # FASTAPI REQUEST
            # ----------------------------------------------

            api_response = requests.post(
                f"{API_URL}/tickets",
                json={
                    "ticket_id": ticket_id,
                    "ticket_text": prompt
                },
                timeout=180
            )

            # ----------------------------------------------
            # CHECK API RESPONSE
            # ----------------------------------------------

            if api_response.status_code != 200:

                status.error(
                    f"API Error: "
                    f"{api_response.status_code}"
                )

                try:

                    st.json(
                        api_response.json()
                    )

                except ValueError:

                    st.write(
                        api_response.text
                    )

                st.stop()

            # ----------------------------------------------
            # GET RESULT
            # ----------------------------------------------

            result = api_response.json()

            # ----------------------------------------------
            # CONTINUE SIMULATION
            # ----------------------------------------------

            status.info(
                "✍️ Response Agent generating response..."
            )

            time.sleep(0.5)

            status.info(
                "🚨 Escalation Agent evaluating ticket..."
            )

            time.sleep(0.5)

            status.info(
                "📊 Learning Agent saving interaction..."
            )

            time.sleep(0.5)

            status.empty()

            # ----------------------------------------------
            # CUSTOMER RESPONSE
            # ----------------------------------------------

            customer_response = result.get(
                "customer_response",
                "Unable to generate a response."
            )

            st.markdown(
                f"""
                <div class="response-box">
                {customer_response}
                </div>
                """,
                unsafe_allow_html=True
            )

            # ----------------------------------------------
            # ESCALATION STATUS
            # ----------------------------------------------

            if result.get(
                "escalation_required",
                False
            ):

                st.warning(
                    "🚨 Ticket escalated — "
                    f"{result.get('escalation_level', 'N/A').upper()}"
                )

            else:

                st.success(
                    "✅ Ticket resolved without escalation."
                )

            # ----------------------------------------------
            # SAVE MESSAGE
            # ----------------------------------------------

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": customer_response,
                    "result": result
                }
            )

            # ----------------------------------------------
            # AGENT LOGS
            # ----------------------------------------------

            with st.expander(
                "🔍 Agent Logs",
                expanded=True
            ):

                st.markdown(
                    "### 🧾 Intake Agent"
                )

                st.write(
                    f"Intent: {result.get('intent', 'N/A')}"
                )

                st.write(
                    f"Sentiment: {result.get('sentiment', 'N/A')}"
                )

                st.markdown(
                    "### 🧠 Classification Agent"
                )

                st.write(
                    f"Category: {result.get('category', 'N/A')}"
                )

                st.write(
                    f"Priority: {result.get('priority', 'N/A')}"
                )

                st.markdown(
                    "### 📊 Confidence"
                )

                confidence = result.get(
                    "classification_confidence",
                    {}
                )

                if confidence:

                    category_conf = float(
                        confidence.get(
                            "category",
                            0
                        )
                    )

                    priority_conf = float(
                        confidence.get(
                            "priority",
                            0
                        )
                    )

                    col1, col2 = st.columns(2)

                    with col1:

                        st.write(
                            f"Category: "
                            f"{category_conf * 100:.2f}%"
                        )

                        st.progress(
                            min(
                                category_conf,
                                1.0
                            )
                        )

                    with col2:

                        st.write(
                            f"Priority: "
                            f"{priority_conf * 100:.2f}%"
                        )

                        st.progress(
                            min(
                                priority_conf,
                                1.0
                            )
                        )

                st.markdown(
                    "### 📚 Retrieval Agent"
                )

                retrieved = result.get(
                    "retrieved_documents",
                    []
                )

                if retrieved:

                    for doc in retrieved:

                        st.write(
                            f"{doc.get('faq_id', 'N/A')} "
                            f"— Score: "
                            f"{doc.get('score', 0):.3f}"
                        )

                else:

                    st.write(
                        "No documents retrieved."
                    )

                st.markdown(
                    "### ✍️ Response Agent"
                )

                st.write(
                    "Model: Ollama / Gemma 3"
                )

                st.write(
                    f"Generated: "
                    f"{result.get('response_generated', False)}"
                )

                st.markdown(
                    "### 🚨 Escalation Agent"
                )

                st.write(
                    f"Required: "
                    f"{result.get('escalation_required', False)}"
                )

                st.write(
                    f"Level: "
                    f"{result.get('escalation_level', 'N/A')}"
                )

                st.write(
                    f"Reason: "
                    f"{result.get('escalation_reason', 'N/A')}"
                )

                st.markdown(
                    "### 📊 Learning Agent"
                )

                st.write(
                    f"Status: "
                    f"{result.get('learning_status', 'N/A')}"
                )

                st.write(
                    f"Database ID: "
                    f"{result.get('database_id', 'N/A')}"
                )

        except requests.exceptions.ConnectionError:

            status.error(
                "❌ Cannot connect to FastAPI."
            )

            st.code(
                "uvicorn src.api.main:app --reload"
            )

        except requests.exceptions.Timeout:

            status.error(
                "⏱️ Request timed out."
            )

        except requests.exceptions.RequestException as e:

            status.error(
                f"API request failed: {e}"
            )

        except Exception as e:

            status.error(
                f"Unexpected error: {e}"
            )