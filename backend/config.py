import os

DB_URL = os.environ.get("DB_URL", "sqlite:///../database/tickets.db?check_same_thread=False&timeout=30")
NOTIFY_EMAIL = "noc_manager@company.com"
