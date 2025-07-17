import time
from rpa_engine import process_tickets

while True:
    process_tickets()
    print("Cycle complete. Sleeping for 2 min.")
    time.sleep(120)
