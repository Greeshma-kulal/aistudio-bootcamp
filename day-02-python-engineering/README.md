# Day 2 – Python Engineering

## Project: Service Ticket Validation System

### Overview
A Python application that reads service ticket records from a CSV file, validates each record using Pydantic, and separates valid and invalid tickets. Logging is used to report validation results.

### Project Structure
```text
day-02-python-engineering/
├── data/
│   └── tickets.csv
├── tickets/
│   ├── __init__.py
│   ├── models.py
│   └── processor.py
├── tests/
│   └── test_processor.py
├── main.py
├── requirements.txt
└── README.md
```

### Technologies Used
- Python 3.12
- Pydantic
- Pytest
- CSV module
- Logging

### Setup

Create and activate a virtual environment:

```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

### Run the Application

```powershell
python main.py
```

The application reads `data/tickets.csv`, validates the records, and displays valid tickets, invalid tickets, and a summary.

### Run Tests

```powershell
python -m pytest -v
```

### Validation Rules
- `ticket_id` must be an integer.
- `equipment` and `issue` are required strings.
- `priority` must be `Low`, `Medium`, or `High`.

### Sample Result
- Valid tickets: 5
- Invalid tickets: 1

The invalid sample record contains the priority `Urgent`, which is rejected by Pydantic validation.

### Learning Outcomes
- Organizing Python code into packages and modules.
- Using type hints and Pydantic models.
- Reading and processing CSV files.
- Handling validation errors.
- Implementing logging.
- Writing unit tests using Pytest.
