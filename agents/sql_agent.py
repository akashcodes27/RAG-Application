"""
SQL Agent — handles structured customer data queries using NL-to-SQL via Gemini.
"""

import os
import sqlite3
import re
from langchain_ollama import ChatOllama

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "database", "customers.db")


# ── Schema Context ────────────────────────────────────────────────────────────

SCHEMA = """
You have access to a SQLite database with the following tables:

TABLE: customers
  customer_id     INTEGER PRIMARY KEY
  name            TEXT
  email           TEXT
  phone           TEXT
  plan            TEXT           -- values: 'Basic', 'Standard', 'Premium'
  country         TEXT
  joined_date     TEXT           -- format: YYYY-MM-DD
  account_status  TEXT           -- values: 'Active', 'Suspended', 'Closed'

TABLE: support_tickets
  ticket_id       INTEGER PRIMARY KEY
  customer_id     INTEGER        -- foreign key to customers
  subject         TEXT
  description     TEXT
  status          TEXT           -- values: 'Open', 'In Progress', 'Resolved', 'Closed'
  priority        TEXT           -- values: 'Low', 'Medium', 'High'
  created_date    TEXT           -- format: YYYY-MM-DD
  resolved_date   TEXT           -- NULL if not yet resolved
  agent_notes     TEXT
"""


def get_schema() -> str:
    return SCHEMA


# ── NL to SQL ─────────────────────────────────────────────────────────────────

def generate_sql(user_question: str) -> str:
    llm = ChatOllama(model="llama3.2", temperature=0)

    prompt = f"""{SCHEMA}

Convert the user's question into a valid SQLite SELECT query.
Output ONLY the raw SQL, no explanation, no markdown, no backticks.
Use LIKE for name searches. Never use DROP/INSERT/UPDATE/DELETE.

User question: {user_question}

SQL:"""

    response = llm.invoke(prompt)
    sql = response.content.strip()
    sql = re.sub(r"```(?:sql)?", "", sql).strip().rstrip("`").strip()
    return sql


def run_sql(sql: str) -> tuple[list, list]:
    """Returns (rows, column_names). Raises on error."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description] if cur.description else []
    conn.close()
    return [dict(r) for r in rows], columns


def format_results_with_llm(user_question: str, rows: list) -> str:
    if not rows:
        return "I searched the customer database but found no matching records."

    llm = ChatOllama(model="llama3.2", temperature=0)
    results_text = "\n".join(str(row) for row in rows)

    prompt = f"""You are a helpful customer support assistant.
The user asked: "{user_question}"

Data retrieved:
{results_text}

Write a clear, friendly response summarising this data. Do not mention SQL or databases."""

    response = llm.invoke(prompt)
    return response.content


def ask_sql_question(user_question: str) -> str:
    try:
        sql = generate_sql(user_question)
        rows, _ = run_sql(sql)
        return format_results_with_llm(user_question, rows)
    except sqlite3.OperationalError as e:
        return f"I had trouble querying the database: {str(e)}"
    except Exception as e:
        return f"Something went wrong: {str(e)}"
