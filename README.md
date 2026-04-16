# Multi-Agent Customer Support AI

A Generative AI–powered multi-agent system that enables natural language interaction with both **structured customer data** (SQL) and **unstructured policy documents** (PDF RAG).

---

## Architecture

```
User Question
      │
      ▼
┌─────────────────┐
│  Router Agent   │  ← classifies intent using Gemini
└────────┬────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌───────┐  ┌───────┐
│  PDF  │  │  SQL  │
│ Agent │  │ Agent │
└───────┘  └───────┘
    │           │
    ▼           ▼
 FAISS       SQLite
 Vector      customers.db
  Store
    │           │
    └─────┬─────┘
          ▼
      Gemini LLM
          │
          ▼
   Natural Language
      Response
```

### Agents
- **Router Agent** — classifies each question as either policy-related (→ PDF Agent) or customer-related (→ SQL Agent)
- **PDF Agent** — chunks PDFs, embeds with HuggingFace `all-MiniLM-L6-v2`, stores in FAISS, retrieves top-4 chunks, answers via Gemini
- **SQL Agent** — converts natural language to SQLite queries via Gemini, executes against `customers.db`, formats results naturally

---

## Project Structure

```
RAG-APPLICATION/
├── app.py                  # Main Streamlit app
├── agents/
│   ├── pdf_agent.py        # PDF RAG pipeline
│   ├── sql_agent.py        # NL-to-SQL pipeline
│   └── router_agent.py     # Intent classifier
├── database/
│   ├── setup_db.py         # Creates + seeds SQLite DB
│   └── customers.db        # Generated database (not committed)
├── htmlTemplate.py         # Chat UI templates
├── .env                    # API keys (not committed)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Setup Instructions

### 1. Clone and create virtual environment

```bash
git clone <your-repo-url>
cd RAG-APPLICATION
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up environment variables

Create a `.env` file in the root directory:

```
GEMINI_API_KEY=your-gemini-api-key-here
```

Get your Gemini API key free at: https://aistudio.google.com/app/apikey

### 4. Seed the database

```bash
python database/setup_db.py
```

This creates `database/customers.db` with 10 synthetic customers and 13 support tickets.

### 5. Run the app

```bash
streamlit run app.py
```

---

## Usage

### Policy Questions (PDF Agent)
1. Upload one or more PDF policy documents using the sidebar
2. Click **Process Documents**
3. Ask questions like:
   - *"What is the refund policy?"*
   - *"How many sick days do employees get?"*
   - *"What happens if I miss 3 days without notice?"*

### Customer Questions (SQL Agent)
No setup needed — works immediately after seeding the DB.
- *"Give me an overview of Ema's profile and her support tickets"*
- *"Show all open high-priority tickets"*
- *"List all customers on the Premium plan"*
- *"Which tickets are unresolved?"*

---

## Tech Stack

| Component | Technology |
|---|---|
| UI | Streamlit |
| LLM | Google Gemini 2.0 Flash |
| Embeddings | HuggingFace `all-MiniLM-L6-v2` |
| Vector Store | FAISS (in-memory) |
| Structured DB | SQLite |
| PDF Parsing | PyPDF2 |
| Text Splitting | LangChain Text Splitters |
| Orchestration | Custom multi-agent routing |

---

## Data

- **Structured data**: 10 synthetic customers with profiles + 13 support tickets stored in SQLite
- **Unstructured data**: Any PDF policy documents uploaded at runtime (sample provided in repo)
