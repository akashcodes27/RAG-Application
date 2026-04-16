# import os
# from langchain_ollama import ChatOllama

# def classify_intent(user_question: str) -> str:
#     llm = ChatOllama(model="llama3.2", temperature=0)

#     prompt = f"""You are a routing assistant. Classify the user's question into one of two categories:

# 1. "pdf" — about company policies, procedures, rules, guidelines, or documents.
# 2. "sql" — about a specific customer, their profile, account, or support tickets.

# Reply with ONLY one word: either "pdf" or "sql". Nothing else.

# Question: {user_question}"""

#     response = llm.invoke(prompt)
#     intent = response.content.strip().lower()
#     if "sql" in intent:
#         return "sql"
#     return "pdf"




# import re
# from langchain_ollama import ChatOllama


# # Keywords that strongly indicate SQL intent
# SQL_KEYWORDS = [
#     "customer", "customers", "account", "ticket", "tickets",
#     "profile", "ema", "james", "sofia", "liam", "amara", "noah",
#     "isla", "raj", "chloe", "marcus", "plan", "premium", "basic",
#     "standard", "suspended", "closed", "active", "unresolved",
#     "open tickets", "support", "database", "record"
# ]


# def classify_intent(user_question: str) -> str:
#     question_lower = user_question.lower()

#     # Keyword check first — fast and reliable
#     for keyword in SQL_KEYWORDS:
#         if keyword in question_lower:
#             return "sql"

#     # Fall back to LLM for ambiguous cases
#     llm = ChatOllama(model="llama3.2", temperature=0)

#     prompt = f"""Classify this question into one of two categories:
# - "pdf": about company policies, rules, procedures, or HR guidelines
# - "sql": about a specific customer, their account, tickets, or database records

# Reply with ONLY one word: pdf or sql.

# Question: {user_question}"""

#     response = llm.invoke(prompt)
#     intent = response.content.strip().lower()
#     if "sql" in intent:
#         return "sql"
#     return "pdf"



import re
from langchain_ollama import ChatOllama

# Strong SQL indicators — customer/ticket specific
SQL_KEYWORDS = [
    "customer", "customers", "account", "ticket", "tickets",
    "profile", "ema", "james", "sofia", "liam", "amara", "noah",
    "isla", "raj", "chloe", "marcus", "plan", "premium", "basic",
    "standard", "suspended", "closed", "active", "unresolved",
    "open tickets", "support ticket", "database", "record", "records",
    "how many customers", "list customers", "show customers"
]

# Strong PDF indicators — policy/document specific
PDF_KEYWORDS = [
    "policy", "policies", "refund", "password", "leave", "vacation",
    "sick", "remote work", "overtime", "harassment", "disciplinary",
    "device", "vpn", "firewall", "cloud", "software", "license",
    "data classification", "incident", "escalation", "sla", "billing dispute",
    "cancellation", "reactivation", "parental", "bereavement", "conduct",
    "handbook", "document", "according to", "what does", "what is the",
    "how many days", "how long", "eligible", "eligibility", "procedure",
    "stolen", "lost device", "phishing", "authentication", "mfa",
    "subscription", "charter"
]


def classify_intent(user_question: str) -> str:
    question_lower = user_question.lower()

    # Count keyword matches for each category
    pdf_score = sum(1 for kw in PDF_KEYWORDS if kw in question_lower)
    sql_score = sum(1 for kw in SQL_KEYWORDS if kw in question_lower)

    if pdf_score > sql_score:
        return "pdf"
    if sql_score > pdf_score:
        return "sql"

    # Tie — fall back to LLM
    llm = ChatOllama(model="llama3.2", temperature=0)

    prompt = f"""Classify this question into exactly one category:
- "pdf": questions about company policies, rules, procedures, refunds, IT security, HR guidelines, or anything from a document
- "sql": questions about a specific customer's name, account details, or support ticket history

Reply with ONLY one word: pdf or sql.

Question: {user_question}"""

    response = llm.invoke(prompt)
    intent = response.content.strip().lower()
    if "sql" in intent:
        return "sql"
    return "pdf"