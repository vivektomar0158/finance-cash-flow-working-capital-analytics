# Data Dictionary

| Table/file | Purpose | Key fields |
|---|---|---|
| `forecast_config` | Scenario controls | `config_key`, `config_value` |
| `opening_cash` | Starting liquidity | `as_of_date`, `opening_cash` |
| `customer_invoices` | Expected receipts | `invoice_id`, `due_date`, `amount`, payment dates |
| `supplier_payments` | Planned supplier outflows | `payment_id`, `payment_date`, `amount` |
| `other_cash_flows` | Payroll, tax, and miscellaneous flows | `flow_type`, `flow_date`, `amount` |
