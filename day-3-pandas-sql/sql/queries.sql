
-- 1. Top 5 vendors by total payment amount
SELECT
    vendor_name,
    SUM(amount) AS total_amount
FROM vendor_payments
GROUP BY vendor_name
ORDER BY total_amount DESC
LIMIT 5;


-- 2. Find duplicate invoice numbers
SELECT
    invoice_number,
    COUNT(*) AS duplicate_count
FROM vendor_payments
GROUP BY invoice_number
HAVING COUNT(*) > 1;


-- 3. Monthly payment totals
SELECT
    DATE_TRUNC('month', payment_date)::DATE AS payment_month,
    SUM(amount) AS monthly_total
FROM vendor_payments
WHERE payment_date IS NOT NULL
GROUP BY DATE_TRUNC('month', payment_date)
ORDER BY payment_month;


-- 4. Find late payments
SELECT
    payment_id,
    vendor_name,
    invoice_number,
    due_date,
    payment_date,
    amount
FROM vendor_payments
WHERE payment_date IS NOT NULL
  AND payment_date > due_date
ORDER BY payment_date;


-- 5. Find unpaid invoices
SELECT *
FROM vendor_payments
WHERE status = 'Pending';


-- 6. Vendors with the highest number of invoices
SELECT
    vendor_name,
    COUNT(*) AS invoice_count
FROM vendor_payments
GROUP BY vendor_name
ORDER BY invoice_count DESC;


-- 7. Calculate the average payment amount
SELECT
    AVG(amount) AS average_payment
FROM vendor_payments;


-- 8. Find payments above the average amount
SELECT *
FROM vendor_payments
WHERE amount > (
    SELECT AVG(amount)
    FROM vendor_payments
)
ORDER BY amount DESC;


-- 9. Total amount by payment status
SELECT
    status,
    COUNT(*) AS transaction_count,
    SUM(amount) AS total_amount
FROM vendor_payments
GROUP BY status;


-- 10. Find overdue pending invoices
SELECT
    payment_id,
    vendor_name,
    invoice_number,
    due_date,
    amount,
    status
FROM vendor_payments
WHERE status = 'Pending'
  AND due_date < CURRENT_DATE
ORDER BY due_date;
