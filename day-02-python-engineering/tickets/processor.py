
import csv
import logging

from pydantic import ValidationError
from tickets.models import Ticket


logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)


def process_csv(file_path: str) -> tuple[list[Ticket], list[dict]]:
    valid_tickets = []
    invalid_tickets = []

    with open(file_path, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row_number, row in enumerate(reader, start=2):
            
            try:
                ticket = Ticket(**row)
                valid_tickets.append(ticket)
                logging.info("Row %d: Ticket %s is valid", row_number, ticket.ticket_id)

            except ValidationError as error:
                invalid_tickets.append({
                    "row": row_number,
                    "data": row,
                    "error": str(error)
                })
                logging.error("Row %d: Invalid ticket", row_number)

    return valid_tickets, invalid_tickets
