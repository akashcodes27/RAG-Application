# Multi-Agent Customer Support AI

A Generative AI–powered multi-agent system that enables a customer support executive to interact with both **structured customer data** (SQL database) and **unstructured policy documents** (PDF knowledge base) through a single natural language interface.

Built as part of a take-home assessment for an AI/ML Developer role.

---

## Demo

> Upload policy PDFs → ask questions → get context-aware answers from the right data source automatically.

**PDF Agent in action:**
- *"What is the refund policy?"* → retrieves and summarises from uploaded policy PDF
- *"What are the password requirements?"* → answers from IT & Cybersecurity Policy

**SQL Agent in action:**
- *"Give me an overview of Ema's profile"* → queries SQLite, returns customer summary
- *"Show all open high priority tickets"* → NL-to-SQL, returns formatted results

---

## Problem Statement

John, a customer support executive, struggles to retrieve information scattered across multiple policy documents and customer databases. This system gives him a single conversational interface to query both sources instantly.

---

## Architecture

```
User Question
      │
      ▼
┌──────────────────────┐
│     Router Agent     │  Keyword scoring + LLM fallback
│   (Intent Classifier)│  → classifies every question as "pdf" or "sql"
└──────────┬───────────┘
           │
     ┌─────┴──────┐
     ▼            ▼
┌─────────┐  ┌─────────┐
│   PDF   │  │   SQL   │
│  Agent  │  │  Agent  │
└────┬────┘  └────┬────┘
     │             │
     ▼             ▼
  FAISS         SQLite
Vector Store   customers.db
(in-memory)   (structured)
     │             │
     └──────┬──────┘
            ▼
       Ollama LLM
     (llama3.2 local)
            │
            ▼
   Natural Language Response
```

### Agent Breakdown

| Agent | Role | Tech |
|---|---|---|
| **Router Agent** | Classifies every question using keyword scoring + LLM fallback | Ollama llama3.2 |
| **PDF Agent** | Chunks PDFs → embeds → retrieves top-4 chunks → generates answer | FAISS + HuggingFace + Ollama |
| **SQL Agent** | Converts NL to SQL → executes → formats results naturally | SQLite + Ollama NL-to-SQL |

---

## Key Technical Features

- **Multi-agent routing** — automatic intent classification with no manual switching required
- **RAG pipeline** — PDF text chunked at 1000 chars with 200 char overlap, embedded with `sentence-transformers/all-MiniLM-L6-v2`, stored in FAISS for semantic retrieval
- **NL-to-SQL** : natural language queries converted to SQLite SELECT statements via LLM, with schema context injection for accuracy
- **Local LLM** : fully offline using Ollama + llama3.2, no API costs, no data leaving the machine
- **Multi-PDF support** — upload and query multiple policy documents simultaneously
- **Persistent chat history** : full conversation maintained in Streamlit session state
- **Graceful fallback** : agents return "not found" responses rather than hallucinating

---

## Tech Stack

| Layer | Technology |
|---|---|
| UI | Streamlit |
| LLM | Ollama (llama3.2) — local, offline |
| Embeddings | HuggingFace `sentence-transformers/all-MiniLM-L6-v2` |
| Vector Store | FAISS (in-memory) |
| Structured DB | SQLite |
| PDF Parsing | PyPDF2 |
| Text Splitting | LangChain Text Splitters |
| LLM Integration | LangChain Ollama |

---

## Project Structure

```
RAG-APPLICATION/
├── app.py                  # Main Streamlit app — UI, routing, chat loop
├── agents/
│   ├── router_agent.py     # Intent classifier (keyword scoring + LLM fallback)
│   ├── pdf_agent.py        # PDF ingestion, FAISS retrieval, answer generation
│   └── sql_agent.py        # NL-to-SQL pipeline, query execution, result formatting
├── database/
│   ├── setup_db.py         # Creates and seeds SQLite with synthetic data
│   └── customers.db        # Generated at setup (not committed to repo)
├── htmlTemplate.py         # Custom chat UI templates (CSS + HTML)
├── .env                    # API keys — not committed
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Dataset

**Structured (SQLite):**
- 10 synthetic customer profiles with name, email, plan, country, account status
- 13 support tickets with subject, description, priority, status, agent notes

**Unstructured (PDFs):**
- `company_policy.pdf` — Employee Policy & Conduct Handbook (HR policies, leave, conduct)
- `IT_Cybersecurity_Policy.pdf` — IT & Security standards (passwords, VPN, devices, incidents)
- `Customer_Service_Refund_Policy.pdf` — Refund eligibility, SLAs, complaint escalation

---

## Setup & Installation

### Prerequisites
- Python 3.10+
- [Ollama](https://ollama.com/download) installed and running

### Steps

```bash
# 1. Clone the repository
git clone <repo-url>
cd RAG-APPLICATION

# 2. Create and activate virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Pull the LLM model
ollama pull llama3.2

# 5. Seed the database (run once)
python database/setup_db.py

# 6. Start the app
streamlit run app.py
```

### Usage
1. Open `http://localhost:8501` in your browser
2. Upload one or more PDF policy documents in the sidebar
3. Click **Process Documents**
4. Ask questions — the system automatically routes to the correct agent

---

## Design Decisions

**Why local LLM (Ollama)?**
Keeps all data on-premise important for enterprise customer support scenarios where policy documents and customer records are sensitive. No API costs, no data sent externally.

**Why SQLite?**
Lightweight, zero configuration, and sufficient for demonstrating NL-to-SQL capabilities. In production this would be replaced with PostgreSQL or any enterprise SQL database — the agent code requires no changes as the interface is abstracted.

**Why keyword scoring for routing?**
LLMs can be inconsistent classifiers for short questions. A hybrid approach  keyword scoring first, LLM fallback for ambiguous cases  gives more reliable routing with lower latency.

**Why FAISS over a managed vector DB?**
For a local, offline setup FAISS is the right tradeoff: no external service dependency, fast enough for document scale retrieval, and trivial to swap for Pinecone or Qdrant in a production deployment.

---

## Requirements

```
streamlit
python-dotenv
PyPDF2
langchain
langchain-community
langchain-text-splitters
langchain-huggingface
langchain-ollama
faiss-cpu
sentence-transformers
```

---

## Author

**Akash** — Masters of Applied Computing, University of Windsor
AI Data Analytics Engineer Co-op @ Gateway Services Inc.
