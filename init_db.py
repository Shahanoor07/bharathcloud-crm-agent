import sqlite3
from datetime import datetime, timedelta

conn = sqlite3.connect("bharathcloud_crm.db")
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS tasks")
cur.execute("DROP TABLE IF EXISTS opportunities")
cur.execute("DROP TABLE IF EXISTS accounts")

cur.execute("""
CREATE TABLE accounts (
    id INTEGER PRIMARY KEY,
    company_name TEXT,
    contact_person TEXT,
    email TEXT,
    industry TEXT,
    assigned_rep TEXT,
    last_contacted_date TEXT
)
""")

cur.execute("""
CREATE TABLE opportunities (
    id INTEGER PRIMARY KEY,
    account_id INTEGER,
    workload_type TEXT,
    monthly_recurring_inr REAL,
    stage TEXT,
    FOREIGN KEY(account_id) REFERENCES accounts(id)
)
""")

cur.execute("""
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER,
    task_description TEXT,
    due_date TEXT,
    status TEXT,
    FOREIGN KEY(account_id) REFERENCES accounts(id)
)
""")

today = datetime.now()

accounts_seed = [
    (1, "Astra MedTech", "Dr. Rajesh", "rajesh@astramed.in", "Healthcare", "Vikram Sen", (today - timedelta(days=10)).strftime('%Y-%m-%d')),
    (2, "PayDirect UPI Gateway", "Anita Nair", "anita@paydirect.com", "Fintech", "Vikram Sen", (today - timedelta(days=3)).strftime('%Y-%m-%d')),
    (3, "Telangana Health Network", "Dr. K. V. Rao", "director@thn.gov.in", "Public Sector", "Vikram Sen", (today - timedelta(days=9)).strftime('%Y-%m-%d')),
    (4, "IndoLogistics ERP", "Siddharth Rao", "sid@indolog.co", "Logistics", "Pooja Reddy", (today - timedelta(days=14)).strftime('%Y-%m-%d')),
    (5, "Kavach Cyber Defense", "Mohan Kumar", "mohan@kavach.ai", "Cybersecurity", "Pooja Reddy", (today - timedelta(days=1)).strftime('%Y-%m-%d')),
    (6, "Deccan FinCorp", "K. Ramana", "ramana@deccanfin.com", "Banking", "Vikram Sen", (today - timedelta(days=12)).strftime('%Y-%m-%d')),
]

opportunities_seed = [
    (1, 1, "Bharath Big Bucket (B3) Storage", 85000.0, "Proposal"),
    (2, 2, "Sovereign Tier-IV Private Cloud", 260000.0, "Architecture Review"),
    (3, 3, "Zero-Downtime Migration & DR", 195000.0, "Proposal"),
    (4, 4, "Kubernetes Managed PaaS", 45000.0, "Qualified"),
    (5, 5, "Virtual Data Center", 70000.0, "Negotiation"),
    (6, 6, "Dedicated Bare Metal Cluster", 340000.0, "Proposal"),
]

cur.executemany("INSERT INTO accounts VALUES (?, ?, ?, ?, ?, ?, ?)", accounts_seed)
cur.executemany("INSERT INTO opportunities VALUES (?, ?, ?, ?, ?)", opportunities_seed)

conn.commit()
conn.close()
print("Relational database initialized successfully.")