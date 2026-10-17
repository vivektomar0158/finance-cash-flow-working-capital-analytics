# Power BI Dashboard Build Guide

## Pages

1. **Executive Cash Outlook:** opening cash, minimum forecast cash, threshold, alert status, and base/stress closing-cash lines.
2. **Weekly Cash Movements:** receipts, payments, net cash flow, and payment-category breakdown.
3. **Scenario Analysis:** base versus stress closing cash, stress gap, first breach week, and delayed receipts.

## Required model fields

Load the SQLite views `v_base_cash_events` and `v_stress_cash_events`. Create a calendar table with week start dates and relate event dates to it.

Recommended measures:

```DAX
Total Receipts = CALCULATE(SUM(CashEvents[amount]), CashEvents[flow_type] = "Receipt")
Total Payments = CALCULATE(SUM(CashEvents[amount]), CashEvents[flow_type] = "Payment")
Net Cash Flow = [Total Receipts] - [Total Payments]
```

Use conditional formatting to show `ALERT` when closing cash is below the configured threshold.
