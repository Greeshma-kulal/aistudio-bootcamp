import pandas as pd
from pathlib import Path

# Locate the CSV file
BASE_DIR = Path(__file__).resolve().parent
CSV_FILE = BASE_DIR / "data" / "vendor_payments.csv"

# 1. Read CSV using Pandas
df = pd.read_csv(CSV_FILE)

print("\n========== VENDOR PAYMENT ANALYSIS ==========")

print("\n1. DATASET OVERVIEW")
print("Dataset shape:", df.shape)
print("\nFirst 5 records:")
print(df.head())

# Convert date columns into datetime format
date_columns = ["invoice_date", "due_date", "payment_date"]

for column in date_columns:
    df[column] = pd.to_datetime(df[column], errors="coerce")

# 2. Group payments by vendor
print("\n2. TOTAL PAYMENT AMOUNT BY VENDOR")

vendor_summary = (
    df.groupby("vendor_name")["amount"]
    .sum()
    .reset_index()
    .sort_values(by="amount", ascending=False)
)

print(vendor_summary.to_string(index=False))

# 3. Monthly payment totals
print("\n3. MONTHLY PAYMENT TOTALS")

paid_df = df[df["payment_date"].notna()].copy()
paid_df["payment_month"] = paid_df["payment_date"].dt.to_period("M")

monthly_summary = (
    paid_df.groupby("payment_month")["amount"]
    .sum()
    .reset_index()
)

print(monthly_summary.to_string(index=False))

# 4. Find pending payments
print("\n4. PENDING PAYMENTS")

pending_df = df[df["status"] == "Pending"]

print(pending_df[
    ["payment_id", "vendor_name", "invoice_number", "amount"]
].to_string(index=False))

# 5. Find late payments
print("\n5. LATE PAYMENTS")

late_df = df[
    (df["payment_date"].notna()) &
    (df["payment_date"] > df["due_date"])
]

print(late_df[
    ["payment_id", "vendor_name", "invoice_number", "due_date", "payment_date"]
].to_string(index=False))

# 6. Find duplicate invoice numbers
print("\n6. DUPLICATE INVOICES")

duplicates = df[df.duplicated(
    subset=["invoice_number"], keep=False
)]

print(duplicates[
    ["payment_id", "vendor_name", "invoice_number"]
].to_string(index=False))

# 7. Demonstrate merge using vendor information
print("\n7. MERGE VENDOR DATA")

vendor_details = pd.DataFrame({
    "vendor_id": [101, 102, 103, 104, 105, 106],
    "vendor_category": [
        "Supplies", "Technology", "Trading",
        "Services", "Logistics", "Digital"
    ]
})

merged_df = pd.merge(
    df,
    vendor_details,
    on="vendor_id",
    how="left"
)

print(merged_df[
    ["vendor_name", "vendor_category", "amount"]
].head(10).to_string(index=False))

print("\n==============================================")
