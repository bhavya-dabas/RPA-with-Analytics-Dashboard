-- Ticket table
CREATE TABLE tickets (
    ticket_id     VARCHAR(50) PRIMARY KEY,
    status        VARCHAR(32),
    created_at    TIMESTAMP,
    escalated     BOOLEAN DEFAULT FALSE,
    sla_breach    BOOLEAN DEFAULT FALSE,
    last_updated  TIMESTAMP
);

-- Processing log table
CREATE TABLE escalation_log (
    log_id        SERIAL PRIMARY KEY,
    ticket_id     VARCHAR(50),
    timestamp     TIMESTAMP,
    action        VARCHAR(32),
    result        VARCHAR(64),
    comment       TEXT
);
