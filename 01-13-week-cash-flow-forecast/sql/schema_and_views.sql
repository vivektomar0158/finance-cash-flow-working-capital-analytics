PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS forecast_config (
    config_key TEXT PRIMARY KEY,
    config_value TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS opening_cash (
    as_of_date TEXT PRIMARY KEY,
    opening_cash REAL NOT NULL CHECK (opening_cash >= 0)
);

CREATE TABLE IF NOT EXISTS customer_invoices (
    invoice_id TEXT PRIMARY KEY,
    customer TEXT NOT NULL,
    invoice_date TEXT NOT NULL,
    due_date TEXT NOT NULL,
    amount REAL NOT NULL CHECK (amount >= 0),
    expected_payment_date TEXT NOT NULL,
    actual_payment_date TEXT,
    payment_status TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS supplier_payments (
    payment_id TEXT PRIMARY KEY,
    vendor TEXT NOT NULL,
    payment_category TEXT NOT NULL,
    payment_date TEXT NOT NULL,
    amount REAL NOT NULL CHECK (amount >= 0),
    payment_status TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS other_cash_flows (
    cash_flow_id TEXT PRIMARY KEY,
    flow_type TEXT NOT NULL CHECK (flow_type IN ('Receipt', 'Payment')),
    category TEXT NOT NULL,
    flow_date TEXT NOT NULL,
    amount REAL NOT NULL CHECK (amount >= 0),
    description TEXT NOT NULL
);

CREATE VIEW IF NOT EXISTS v_customer_receipts AS
SELECT
    CASE
        WHEN actual_payment_date IS NOT NULL THEN actual_payment_date
        WHEN expected_payment_date < (SELECT config_value FROM forecast_config WHERE config_key = 'as_of_date') THEN (SELECT config_value FROM forecast_config WHERE config_key = 'as_of_date')
        ELSE expected_payment_date
    END AS settlement_date,
    amount,
    customer,
    'Base' AS scenario
FROM customer_invoices;

CREATE VIEW IF NOT EXISTS v_base_cash_events AS
SELECT settlement_date AS event_date, amount, 'Receipt' AS flow_type, customer AS source, scenario FROM v_customer_receipts
UNION ALL
SELECT payment_date, amount, 'Payment', vendor, 'Base' FROM supplier_payments
UNION ALL
SELECT flow_date, amount, flow_type, category, 'Base' FROM other_cash_flows;

CREATE VIEW IF NOT EXISTS v_stress_cash_events AS
SELECT
    CASE
        WHEN actual_payment_date IS NOT NULL THEN actual_payment_date
        ELSE date(expected_payment_date, '+' || (SELECT config_value FROM forecast_config WHERE config_key = 'stress_delay_days') || ' days')
    END AS event_date,
    amount,
    'Receipt' AS flow_type,
    customer AS source,
    'Customer_Payments_20_Days_Late' AS scenario
FROM customer_invoices
UNION ALL
SELECT payment_date, amount, 'Payment', vendor, 'Customer_Payments_20_Days_Late' FROM supplier_payments
UNION ALL
SELECT flow_date, amount, flow_type, category, 'Customer_Payments_20_Days_Late' FROM other_cash_flows;
