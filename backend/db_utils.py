from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from config import DB_URL
import datetime

engine = create_engine(DB_URL, future=True)
Session = sessionmaker(bind=engine)

def fetch_tickets():
    with engine.connect() as conn:
        result = conn.execute(text(
            "SELECT * FROM tickets WHERE status='Open' AND escalated=FALSE;"
        ))
        return [dict(row) for row in result]

def update_ticket(ticket_id, escalate=True):
    now = datetime.datetime.now()
    status = "Escalated" if escalate else "Checked"
    with engine.begin() as conn:
        conn.execute(
            text("UPDATE tickets SET escalated=:esc, last_updated=:ts WHERE ticket_id=:tid"),
            dict(esc=escalate, ts=now, tid=ticket_id)
        )
        action = "API_update"
        result = "Success"
        log_action(ticket_id, action, result, f"Updated via backend at {now}")
    return status

def log_action(ticket_id, action, result, comment):
    now = datetime.datetime.now()
    with engine.begin() as conn:
        conn.execute(
            text("INSERT INTO escalation_log (ticket_id,timestamp,action,result,comment) VALUES(:tid,:ts,:ac,:res,:com)"),
            dict(tid=ticket_id, ts=now, ac=action, res=result, com=comment)
        )

def get_stats():
    with engine.connect() as conn:
        tickets_open = conn.execute(text(
            "SELECT count(*) FROM tickets WHERE status='Open';"
        )).scalar()
        escalations_today = conn.execute(text(
            "SELECT count(*) FROM escalation_log WHERE action='API_update' AND DATE(timestamp)=DATE('now');"
        )).scalar()
        sla_breach = conn.execute(text(
            "SELECT count(*) FROM tickets WHERE sla_breach=TRUE;"
        )).scalar()
        return {
            "tickets_open": tickets_open,
            "escalations_today": escalations_today,
            "sla_breach": sla_breach
        }

def fetch_logs(limit=10):
    with engine.connect() as conn:
        result = conn.execute(text(
            "SELECT * FROM escalation_log ORDER BY timestamp DESC LIMIT :l"
        ), dict(l=limit))
        return [dict(row) for row in result]
