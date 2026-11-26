# Day 3 – Pandas and PostgreSQL

## Project Overview
This project analyzes a synthetic vendor payments dataset using Python Pandas and PostgreSQL. It identifies payment trends, duplicate invoices, pending payments, and late payments.

## Project Structure
```text
day-3-pandas-sql/
├── data/
│   └── vendor_payments.csv
├── sql/
│   └── queries.sql
├── pandas_analysis.py
├── insights.md
├── requirements.txt
└── README.md
```

## Technologies Used
- Python 3.12
- Pandas
- PostgreSQL
- pgAdmin 4
- SQL

## Dataset
The dataset contains 20 synthetic vendor payment records with details such as vendor ID, invoice number, invoice date, due date, payment date, amount, and payment status.

## Pandas Analysis
The `pandas_analysis.py` script performs:
- Dataset loading and overview
- Vendor-wise payment totals using groupby
- Monthly payment analysis
- Identification of pending payments
- Identification of late payments
- Duplicate invoice detection
- Merging vendor details using vendor ID

## PostgreSQL Analysis
The dataset was imported into a PostgreSQL database named `vendor_payments_db`, in the `vendor_payments` table.

The `sql/queries.sql` file contains 10 queries covering:
- Top vendors by payment amount
- Duplicate invoices
- Monthly payment totals
- Late payments
- Pending invoices
- Invoice counts by vendor
- Average payment amount
- Payments above average
- Payment totals by status
- Overdue pending invoices

## Setup and Execution

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the Pandas analysis:
   ```bash
   python pandas_analysis.py
   ```

3. Execute the SQL queries using pgAdmin 4 after connecting to `vendor_payments_db`.

## Key Findings
Refer to `insights.md` for the findings from the dataset analysis.