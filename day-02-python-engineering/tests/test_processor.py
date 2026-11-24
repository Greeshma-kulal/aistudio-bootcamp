import pytest
from pydantic import ValidationError

from tickets.models import Ticket
from tickets.processor import process_csv


def test_valid_ticket():
    ticket = Ticket(
        ticket_id=101,
        equipment="Printer",
        issue="Paper jam",
        priority="High"
    )
    assert ticket.ticket_id == 101


def test_invalid_priority():
    with pytest.raises(ValidationError):
        Ticket(
            ticket_id=102,
            equipment="Router",
            issue="Slow internet",
            priority="Urgent"
        )


def test_missing_required_field():
    with pytest.raises(ValidationError):
        Ticket(
            ticket_id=103,
            equipment="Scanner",
            priority="Low"
        )


def test_invalid_ticket_id():
    with pytest.raises(ValidationError):
        Ticket(
            ticket_id="abc",
            equipment="Laptop",
            issue="Battery problem",
            priority="High"
        )


def test_process_csv(tmp_path):
    csv_file = tmp_path / "test_tickets.csv"

    csv_file.write_text(
        "ticket_id,equipment,issue,priority\n"
        "101,Printer,Paper jam,High\n"
        "102,Router,Slow internet,Urgent\n",
        encoding="utf-8"
    )

    valid, invalid = process_csv(str(csv_file))

    assert len(valid) == 1
    assert len(invalid) == 1