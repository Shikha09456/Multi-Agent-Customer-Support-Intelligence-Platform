```markdown
# 🤖 Multi-Agent Customer Support Intelligence Platform

An intelligent, end-to-end **Multi-Agent Customer Support System** designed to automate customer ticket analysis, knowledge retrieval, response generation, escalation, and interaction logging.

The platform uses **LangGraph** to orchestrate specialized AI agents, **FAISS + Sentence Transformers** for Retrieval-Augmented Generation (RAG), **Ollama + Gemma 3** for grounded response generation, **PostgreSQL** for interaction storage, **FastAPI** for backend APIs, and **Streamlit** for the customer-support chat interface.

---

## 🚀 Project Overview

Modern e-commerce platforms receive thousands of customer-support tickets related to:

- Delivery issues
- Order problems
- Refunds
- Product issues
- Cancellations
- Payments
- Complaints
- Other customer-service requests

Handling these tickets manually can be slow, inconsistent, and difficult to scale.

This project solves the problem using a **multi-agent architecture**, where each agent is responsible for a specific stage of the customer-support workflow.

### Core Workflow

```text
                    Customer Ticket
                          │
                          ▼
                  🧾 Intake Agent
                          │
                          ▼
              🧠 Classification Agent
                          │
                          ▼
                  📚 Retrieval Agent
                       (RAG)
                          │
                          ▼
                  ✍️ Response Agent
                          │
                          ▼
                 🚨 Escalation Agent
                          │
                          ▼
                📊 Learning Agent
                          │
                          ▼
                    PostgreSQL
```

The workflow is implemented using **LangGraph** as a sequential multi-agent workflow.

---

# 🧠 Multi-Agent Architecture

Each agent has a dedicated responsibility.

## 1. 🧾 Intake Agent

The Intake Agent processes the raw customer ticket.

### Responsibilities

- Clean customer text
- Identify customer intent
- Analyze sentiment
- Extract important entities
- Extract order IDs
- Identify products

### Example

```text
Input:
"My order ORD123 hasn't arrived yet and I'm really frustrated."

Output:

Intent:
delivery_issue

Sentiment:
Negative

Entities:
order_id = ORD123
```

---

## 2. 🧠 Classification Agent

The Classification Agent determines:

- Ticket category
- Ticket priority
- Classification confidence

### Example

```text
Category:
Delivery Issue

Priority:
High

Confidence:
Category → 0.29
Priority → 0.54
```

The confidence scores are also used by the Escalation Agent to identify uncertain predictions.

---

## 3. 📚 Retrieval Agent

The Retrieval Agent implements the project's **RAG pipeline**.

### Pipeline

```text
Customer Ticket
      │
      ▼
Sentence Transformer
      │
      ▼
Embedding
      │
      ▼
FAISS Vector Search
      │
      ▼
Relevant FAQ Documents
      │
      ▼
Response Agent
```

### Technologies

- Sentence Transformers
- `all-MiniLM-L6-v2`
- FAISS
- FAQ knowledge base

The system retrieves the most relevant documents before generating a response.

---

## 4. ✍️ Response Agent

The Response Agent generates the final customer-facing response.

The response is generated using:

**Ollama + Gemma 3 4B**

The model receives:

- Customer ticket
- Intent
- Sentiment
- Category
- Priority
- Retrieved FAQ documents

The response prompt is designed to keep the answer grounded in the retrieved knowledge.

### Grounding Rules

The Response Agent is instructed to:

- Use retrieved information
- Avoid inventing policies
- Avoid inventing refunds or compensation
- Avoid inventing dates
- Avoid exposing internal system information
- Provide a professional customer-support response

---

## 5. 🚨 Escalation Agent

The Escalation Agent determines whether the ticket should be escalated to a human support representative.

### Escalation Signals

The agent considers:

- Ticket priority
- Customer sentiment
- Classification confidence
- Retrieval quality
- Availability of relevant documents

### Example

```text
Priority:
High

Sentiment:
Negative

Category Confidence:
0.29

Priority Confidence:
0.54

Escalation:
TRUE

Level:
HIGH
```

### Escalation Levels

```text
NONE
MEDIUM
HIGH
CRITICAL
```

The agent also generates an explanation for why escalation was triggered.

---

## 6. 📊 Learning Agent

The Learning Agent stores the completed interaction in PostgreSQL.

The stored information includes:

- Ticket information
- Intent
- Sentiment
- Category
- Priority
- Retrieved documents
- Customer response
- Escalation decision
- Escalation level
- Escalation reason
- Customer feedback fields
- Prompt information
- Timestamps

This creates a persistent interaction history that can later be used for system evaluation and improvement.

---

# 🔄 LangGraph Workflow

The complete workflow is implemented using LangGraph.

```text
START
  │
  ▼
Intake
  │
  ▼
Classification
  │
  ▼
Retrieval
  │
  ▼
Response
  │
  ▼
Escalation
  │
  ▼
Learning
  │
  ▼
END
```

### Why LangGraph?

LangGraph provides:

- Explicit workflow orchestration
- Stateful execution
- Agent-to-agent coordination
- Structured state management
- Easy extension of future agents
- Clear separation of responsibilities

The complete workflow operates on a shared `TicketState`.

---

# 🗂️ Project Structure

```text
Multi-Agent-Customer-Support-Intelligence-Platform/
│
├── app/
│   └── streamlit_app.py
│
├── data/
│   ├── knowledge_base/
│   │   └── README.md
│   │
│   └── vector_store/
│       ├── README.md
│       └── faq_faiss.index
│
├── models/
│   └── README.md
│
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_data_preprocessing.ipynb
│   ├── 03_model_training (1).ipynb
│   └── 04_rag_indexing.ipynb
│
├── src/
│   ├── agents/
│   │   ├── classification_agent.py
│   │   ├── escalation_agent.py
│   │   ├── intake_agent.py
│   │   ├── learning_agent.py
│   │   ├── response_agent.py
│   │   └── retrieval_agent.py
│   │
│   ├── api/
│   │   ├── main.py
│   │   └── schemas.py
│   │
│   ├── rag/
│   │   ├── embeddings.py
│   │   ├── retriever.py
│   │   └── vector_store.py
│   │
│   ├── workflow/
│   │   └── workflow.py
│   │
│   ├── config.py
│   ├── database.py
│   └── state.py
│
├── test_learning_agent.py
├── test_response_agent.py
├── test_workflow.py
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

# 🛠️ Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Agent Orchestration | LangGraph |
| LLM | Gemma 3 4B |
| Local LLM Runtime | Ollama |
| RAG | FAISS |
| Embeddings | Sentence Transformers |
| Embedding Model | all-MiniLM-L6-v2 |
| ML | Scikit-learn |
| Backend API | FastAPI |
| Frontend | Streamlit |
| Database | PostgreSQL |
| Database Driver | psycopg |
| Workflow State | TypedDict |
| API Server | Uvicorn |

---

# 🧩 Machine Learning Components

The project uses machine-learning models for ticket intelligence.

### Classification

The classification system predicts:

```text
Ticket Category
Ticket Priority
```

### Sentiment Analysis

Customer messages are analyzed to identify sentiment such as:

```text
Positive
Negative
Neutral
```

### Confidence-Based Decision Making

Instead of relying only on predictions, the system also considers model confidence.

For example:

```text
Category Confidence = 0.29
Priority Confidence = 0.54
```

Low-confidence predictions can contribute to escalation.

---

# 📚 RAG Pipeline

The project uses Retrieval-Augmented Generation to ground customer responses in a knowledge base.

### Indexing

```text
FAQ Documents
      │
      ▼
Text Processing
      │
      ▼
Sentence Transformer
      │
      ▼
Embeddings
      │
      ▼
FAISS Index
```

### Retrieval

```text
Customer Query
      │
      ▼
Query Embedding
      │
      ▼
FAISS Similarity Search
      │
      ▼
Top-K Documents
      │
      ▼
Response Generation
```

The current retrieval system uses:

```text
Top-K = 5
```

---

# 🗄️ PostgreSQL Database

The system stores customer-support interactions in PostgreSQL.

### Main Table

```text
support_interactions
```

### Stored Information

```text
ticket_id
ticket_text
cleaned_text
intent
sentiment
category
priority
order_id
product
retrieved_documents
customer_response
escalation_required
escalation_level
escalation_reason
resolution_text
customer_satisfaction_score
retrieval_feedback
human_feedback
prompt_strategy
prompt_version
created_at
resolved_at
```

This allows the platform to maintain a history of processed tickets and their outcomes.

---

# 🌐 FastAPI

FastAPI exposes the multi-agent workflow through an API.

### Start the API

```bash
uvicorn src.api.main:app --reload
```

The API will run at:

```text
http://127.0.0.1:8000
```

### Swagger Documentation

```text
http://127.0.0.1:8000/docs
```

### Main Endpoint

```http
POST /tickets
```

Example request:

```json
{
    "ticket_id": "TICKET_001",
    "ticket_text": "My order has not arrived yet."
}
```

The API executes the complete multi-agent workflow and returns the processed result.

---

# 💬 Streamlit Chat Interface

The project includes a Streamlit-based customer-support chat interface.

### Start Streamlit

```bash
streamlit run app/streamlit_app.py
```

Open:

```text
http://localhost:8501
```

### UI Features

The interface provides:

- 💬 Chat-style customer interaction
- 🎫 Automatic ticket IDs
- 🧠 Classification results
- 📊 Confidence scores
- 📚 Retrieved FAQ documents
- ✍️ Generated customer response
- 🚨 Escalation information
- 📋 Expandable agent logs
- 💾 Persistent backend logging

---

# 🧪 Testing

The project contains tests for important components.

### Workflow Test

```bash
python test_workflow.py
```

### Response Agent Test

```bash
python test_response_agent.py
```

### Learning Agent Test

```bash
python test_learning_agent.py
```

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/Shikha09456/Multi-Agent-Customer-Support-Intelligence-Platform.git
```

```bash
cd Multi-Agent-Customer-Support-Intelligence-Platform
```

---

## 2. Create Virtual Environment

Windows:

```powershell
python -m venv .venv
```

Activate:

```powershell
.venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔐 Environment Variables

Create a `.env` file in the project root.

Example:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=customer_support_db
DB_USER=postgres
DB_PASSWORD=your_password

OLLAMA_URL=http://localhost:11434/api/generate
OLLAMA_MODEL=gemma3:4b
```

Never commit `.env` to GitHub.

Use `.env.example` as the template.

---

# 🐘 PostgreSQL Setup

Create the database:

```sql
CREATE DATABASE customer_support_db;
```

Make sure PostgreSQL is running before starting the application.

The application uses PostgreSQL for persistent interaction logging.

---

# 🦙 Ollama Setup

Install Ollama and download the Gemma model.

```bash
ollama pull gemma3:4b
```

Start Ollama:

```bash
ollama serve
```

Verify:

```bash
ollama list
```

The Response Agent communicates with Ollama through its local API.

---

# ▶️ Running the Complete Application

You need two terminals.

### Terminal 1 — FastAPI

```powershell
.venv\Scripts\activate
uvicorn src.api.main:app --reload
```

### Terminal 2 — Streamlit

```powershell
.venv\Scripts\activate
streamlit run app/streamlit_app.py
```

Then open:

```text
http://localhost:8501
```

---

# 🔍 Example Workflow

### Customer Input

```text
"My order ORD123 hasn't arrived and I am very frustrated."
```

### Intake Agent

```text
Intent: delivery_issue
Sentiment: Negative
Order ID: ORD123
```

### Classification Agent

```text
Category: Delivery Issue
Priority: High
```

### Retrieval Agent

Retrieves relevant delivery-related FAQs.

### Response Agent

Generates a grounded customer response using Gemma 3.

### Escalation Agent

Evaluates:

```text
Priority
Sentiment
Classification Confidence
Retrieval Quality
```

and determines whether human escalation is required.

### Learning Agent

Stores the complete interaction in PostgreSQL.

---

# 🎯 Key Features

- ✅ Multi-agent customer support architecture
- ✅ LangGraph workflow orchestration
- ✅ Stateful agent execution
- ✅ ML-based ticket classification
- ✅ Sentiment analysis
- ✅ Confidence-aware decision making
- ✅ FAISS-based semantic retrieval
- ✅ RAG-powered responses
- ✅ Local LLM using Ollama
- ✅ Gemma 3 integration
- ✅ Escalation intelligence
- ✅ PostgreSQL interaction logging
- ✅ FastAPI backend
- ✅ Streamlit chat interface
- ✅ Agent execution logs
- ✅ Automated workflow testing

---

# 🔮 Future Improvements

The architecture can be extended with:

- Human-in-the-loop review
- Customer feedback collection
- Automated model evaluation
- Retrieval quality monitoring
- Response quality evaluation
- Agent performance analytics
- Automatic retraining pipelines
- Better escalation policies
- Authentication and authorization
- Docker deployment
- Cloud deployment
- Monitoring and observability
- Production-scale vector databases
- Advanced multi-agent routing

---

# 🏗️ Architecture Philosophy

The project follows a **specialized-agent architecture** rather than using one large agent for every task.

Each agent has a focused responsibility:

```text
Intake
  ↓
Understand the ticket

Classification
  ↓
Determine category + priority

Retrieval
  ↓
Find relevant knowledge

Response
  ↓
Generate grounded answer

Escalation
  ↓
Determine human intervention

Learning
  ↓
Store interaction
```

This separation makes the system easier to:

- Debug
- Test
- Extend
- Monitor
- Improve
- Deploy

---

# 📌 Project Status

### Core System

**Completed ✅**

- Multi-agent workflow
- LangGraph orchestration
- Ticket intake
- Classification
- Sentiment analysis
- RAG retrieval
- LLM response generation
- Escalation logic
- PostgreSQL logging
- FastAPI API
- Streamlit chat interface
- Agent logging
- Component testing

### Planned

- Advanced feedback loop
- Performance analytics
- Human-in-the-loop evaluation
- Automated model improvement
- Production deployment

---

# 👩‍💻 Author

**Shikha Kumari**

AI / ML & Generative AI Enthusiast

Areas of interest:

- Artificial Intelligence
- Machine Learning
- Generative AI
- Agentic AI
- Multi-Agent Systems
- RAG
- LangGraph
- LLM Applications

---

# ⭐ If You Find This Project Useful

Feel free to explore the repository, raise issues, and suggest improvements.

If you find the project interesting, consider giving it a ⭐ on GitHub.
```

### One correction before you commit this

Tumhare current repo me `scripts/` ki files **empty** hain, according to what you told me. Isliye README me unko functional scripts ki tarah describe karna avoid karna better hoga.

Also, since you decided **analytics ko abhi postpone karna hai**, README me `src/analytics/` ko **future/planned component** ke roop me mention karna cleaner hoga rather than presenting it as completed.

If you want the README to accurately reflect the **current final project only**, I recommend removing `src/analytics/` from the project-structure section before the final GitHub push.
