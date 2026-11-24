
from pathlib import Path

from tickets.processor import process_csv


# Locate the CSV file
BASE_DIR = Path(__file__).resolve().parent
CSV_FILE = BASE_DIR / "data" / "tickets.csv"


def main():
    print("\n========== SERVICE TICKET VALIDATION ==========")

    valid_tickets, invalid_tickets = process_csv(str(CSV_FILE))

    print("\n---------- VALID TICKETS ----------")
    for ticket in valid_tickets:
        print(ticket.model_dump())

    print("\n---------- INVALID TICKETS ----------")
    if invalid_tickets:
        for ticket in invalid_tickets:
            print(ticket)
    else:
        print("No invalid tickets found.")

    print("\n---------- SUMMARY ----------")
    print(f"Total valid tickets: {len(valid_tickets)}")
    print(f"Total invalid tickets: {len(invalid_tickets)}")
    print("===============================================")


if __name__ == "__main__":
    main()
