PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS reporting_dates (reporting_date TEXT PRIMARY KEY, days_in_period INTEGER NOT NULL, dso_improvement_days INTEGER NOT NULL);
CREATE TABLE IF NOT EXISTS customers (customer_id TEXT PRIMARY KEY, customer_name TEXT NOT NULL, segment TEXT NOT NULL, region TEXT NOT NULL, credit_limit REAL NOT NULL, payment_terms_days INTEGER NOT NULL);
CREATE TABLE IF NOT EXISTS vendors (vendor_id TEXT PRIMARY KEY, vendor_name TEXT NOT NULL, category TEXT NOT NULL, payment_terms_days INTEGER NOT NULL);
CREATE TABLE IF NOT EXISTS sales_invoices (invoice_id TEXT PRIMARY KEY, customer_id TEXT NOT NULL REFERENCES customers(customer_id), invoice_date TEXT NOT NULL, due_date TEXT NOT NULL, invoice_amount REAL NOT NULL, currency TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS customer_payments (payment_id TEXT PRIMARY KEY, invoice_id TEXT NOT NULL REFERENCES sales_invoices(invoice_id), payment_date TEXT NOT NULL, payment_amount REAL NOT NULL);
CREATE TABLE IF NOT EXISTS purchase_bills (bill_id TEXT PRIMARY KEY, vendor_id TEXT NOT NULL REFERENCES vendors(vendor_id), bill_date TEXT NOT NULL, due_date TEXT NOT NULL, bill_amount REAL NOT NULL, currency TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS supplier_payments (payment_id TEXT PRIMARY KEY, bill_id TEXT NOT NULL REFERENCES purchase_bills(bill_id), payment_date TEXT NOT NULL, payment_amount REAL NOT NULL);
CREATE TABLE IF NOT EXISTS inventory_snapshots (snapshot_date TEXT PRIMARY KEY, inventory_value REAL NOT NULL);
CREATE TABLE IF NOT EXISTS monthly_financials (period_start TEXT PRIMARY KEY, credit_sales REAL NOT NULL, cogs REAL NOT NULL);
