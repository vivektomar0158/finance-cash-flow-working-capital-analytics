DROP VIEW IF EXISTS ar_open_items;
CREATE VIEW ar_open_items AS
SELECT
    invoice.invoice_id,
    invoice.customer_id,
    invoice.invoice_amount - COALESCE(SUM(payment.payment_amount), 0) AS open_balance,
    CAST(julianday((SELECT reporting_date FROM reporting_dates LIMIT 1)) - julianday(invoice.due_date) AS INTEGER) AS days_past_due,
    invoice.due_date
FROM sales_invoices invoice
LEFT JOIN customer_payments payment ON payment.invoice_id = invoice.invoice_id
GROUP BY invoice.invoice_id
HAVING open_balance > 0;

DROP VIEW IF EXISTS ar_aging;
CREATE VIEW ar_aging AS
SELECT
    item.*,
    CASE
        WHEN days_past_due <= 0 THEN 'Current'
        WHEN days_past_due BETWEEN 1 AND 30 THEN '1-30'
        WHEN days_past_due BETWEEN 31 AND 60 THEN '31-60'
        WHEN days_past_due BETWEEN 61 AND 90 THEN '61-90'
        ELSE '90+'
    END AS aging_bucket
FROM ar_open_items item;

DROP VIEW IF EXISTS ap_open_items;
CREATE VIEW ap_open_items AS
SELECT
    bill.bill_id,
    bill.vendor_id,
    bill.bill_amount - COALESCE(SUM(payment.payment_amount), 0) AS open_balance,
    CAST(julianday((SELECT reporting_date FROM reporting_dates LIMIT 1)) - julianday(bill.due_date) AS INTEGER) AS days_past_due,
    bill.due_date
FROM purchase_bills bill
LEFT JOIN supplier_payments payment ON payment.bill_id = bill.bill_id
GROUP BY bill.bill_id
HAVING open_balance > 0;
