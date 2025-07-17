import os

DB_URL = os.environ.get("DB_URL", "sqlite:///../database/tickets.db")
NOTIFY_EMAIL = "noc_manager@company.com"
