from db_utils import fetch_tickets, update_ticket, log_action
from ui_automation import escalate_ticket_ui
from notification_utils import send_alert

def process_tickets():
    tickets = fetch_tickets()
    for t in tickets:
        ticket_id = t['ticket_id']
        try:
            status = update_ticket(ticket_id)
            log_action(ticket_id, "API_update", "Success", "Escalated via API.")
        except Exception as e:
            try:
                ui_result = escalate_ticket_ui(t)
                log_action(ticket_id, "UI_update", "Success", "Escalated via UI fallback.")
            except Exception as ui_e:
                log_action(ticket_id, "FAIL", "Fail", str(ui_e))
                send_alert(
                    f"Ticket Escalation Failed: {ticket_id}",
                    f"API and UI escalation failed. Error: {str(ui_e)}"
                )

if __name__ == "__main__":
    process_tickets()
