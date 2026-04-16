"""
Run this once to create and seed the SQLite database.
Usage: python database/setup_db.py
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "customers.db")


def create_and_seed():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # ── Tables ────────────────────────────────────────────────────────────────
    cur.executescript("""
    DROP TABLE IF EXISTS customers;
    DROP TABLE IF EXISTS support_tickets;

    CREATE TABLE customers (
        customer_id     INTEGER PRIMARY KEY,
        name            TEXT NOT NULL,
        email           TEXT UNIQUE NOT NULL,
        phone           TEXT,
        plan            TEXT,
        country         TEXT,
        joined_date     TEXT,
        account_status  TEXT
    );

    CREATE TABLE support_tickets (
        ticket_id       INTEGER PRIMARY KEY,
        customer_id     INTEGER NOT NULL,
        subject         TEXT,
        description     TEXT,
        status          TEXT,
        priority        TEXT,
        created_date    TEXT,
        resolved_date   TEXT,
        agent_notes     TEXT,
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
    );
    """)

    # ── Customers ─────────────────────────────────────────────────────────────
    customers = [
        (1, "Ema Thompson",    "ema.thompson@email.com",    "+1-555-0101", "Premium",  "USA",     "2022-03-15", "Active"),
        (2, "James Patel",     "james.patel@email.com",     "+1-555-0102", "Standard", "Canada",  "2021-07-22", "Active"),
        (3, "Sofia Reyes",     "sofia.reyes@email.com",     "+52-555-0103","Premium",  "Mexico",  "2023-01-10", "Active"),
        (4, "Liam Chen",       "liam.chen@email.com",       "+1-555-0104", "Basic",    "USA",     "2020-11-05", "Suspended"),
        (5, "Amara Osei",      "amara.osei@email.com",      "+233-555-0105","Standard","Ghana",   "2022-08-30", "Active"),
        (6, "Noah Williams",   "noah.williams@email.com",   "+1-555-0106", "Premium",  "USA",     "2019-04-18", "Active"),
        (7, "Isla Murphy",     "isla.murphy@email.com",     "+353-555-0107","Basic",   "Ireland", "2023-06-25", "Active"),
        (8, "Raj Sharma",      "raj.sharma@email.com",      "+91-555-0108", "Standard","India",   "2021-12-01", "Active"),
        (9, "Chloe Dubois",    "chloe.dubois@email.com",    "+33-555-0109", "Premium", "France",  "2022-05-14", "Active"),
        (10,"Marcus Green",    "marcus.green@email.com",    "+1-555-0110",  "Basic",   "USA",     "2020-09-09", "Closed"),
    ]

    cur.executemany("""
        INSERT INTO customers VALUES (?,?,?,?,?,?,?,?)
    """, customers)

    # ── Support Tickets ───────────────────────────────────────────────────────
    tickets = [
        (1,  1, "Billing overcharge on March invoice",
             "Customer was charged twice for the monthly subscription fee in March.",
             "Resolved", "High",   "2024-03-18", "2024-03-20",
             "Refund of $49.99 processed. Root cause: duplicate billing cycle trigger."),

        (2,  1, "Cannot access premium features",
             "Customer reports that premium dashboard features are unavailable after renewal.",
             "Resolved", "Medium", "2024-05-02", "2024-05-03",
             "Account flag cleared. Features restored after cache reset on backend."),

        (3,  1, "Request to upgrade plan",
             "Customer wants to add a second user seat to her Premium plan.",
             "Open",     "Low",    "2024-11-10", None,
             "Awaiting confirmation of pricing from sales team."),

        (4,  2, "Login failure after password reset",
             "Customer is unable to log in after completing a password reset.",
             "Resolved", "High",   "2024-01-15", "2024-01-15",
             "Session token was stale. Force logout across devices resolved the issue."),

        (5,  2, "Data export not working",
             "CSV export button returns an empty file for date ranges over 90 days.",
             "In Progress","Medium","2024-10-05", None,
             "Engineering confirmed a pagination bug. Fix targeted for next sprint."),

        (6,  3, "Refund request for unused subscription month",
             "Customer travelled and did not use the service for 30 days, requesting partial refund.",
             "Resolved", "Medium", "2024-07-22", "2024-07-25",
             "Partial credit of $24.99 issued as per refund policy section 3.2."),

        (7,  4, "Account suspended without notice",
             "Customer claims the account was suspended without any prior warning email.",
             "Open",     "High",   "2024-09-01", None,
             "Suspension triggered by 3 failed payment attempts. Customer notified via email per policy."),

        (8,  5, "Integration with third-party CRM not syncing",
             "Salesforce integration stopped syncing contact updates after Oct 1 update.",
             "In Progress","High", "2024-10-12", None,
             "API key rotation broke the webhook. Customer provided new key, testing in progress."),

        (9,  6, "Feature request: dark mode",
             "Customer requests a dark mode option for the dashboard.",
             "Closed",   "Low",    "2024-04-03", "2024-04-10",
             "Logged as feature request in product backlog. Customer notified."),

        (10, 7, "Invoice PDF not downloading",
             "Download invoice button gives a 404 error for invoices older than 6 months.",
             "Resolved", "Medium", "2024-08-19", "2024-08-20",
             "Storage bucket policy misconfiguration fixed. All old invoices accessible again."),

        (11, 8, "Wrong currency displayed on invoices",
             "Invoices show USD instead of INR despite region being set to India.",
             "Resolved", "Low",    "2024-06-05", "2024-06-07",
             "Currency locale setting was not applied to invoice renderer. Fixed in v2.3.1."),

        (12, 9, "Agent response time too slow",
             "Customer reports waiting over 48 hours for a response on ticket #8.",
             "Resolved", "High",   "2024-10-15", "2024-10-16",
             "Escalated to senior agent. SLA breach acknowledged, compensation credit applied."),

        (13, 10,"Request to reopen closed account",
             "Former customer wants to reactivate their account and migrate old data.",
             "Open",     "Medium", "2024-11-01", None,
             "Data retention policy allows reactivation within 12 months. Verification pending."),
    ]

    cur.executemany("""
        INSERT INTO support_tickets VALUES (?,?,?,?,?,?,?,?,?)
    """, tickets)

    conn.commit()
    conn.close()
    print(f"Database created at: {DB_PATH}")
    print(f"  → {len(customers)} customers seeded")
    print(f"  → {len(tickets)} support tickets seeded")


if __name__ == "__main__":
    create_and_seed()
