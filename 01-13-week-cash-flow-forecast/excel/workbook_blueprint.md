# Excel Workbook Blueprint

Create `13_week_cash_forecast.xlsx` with these sheets:

1. **Control Panel** — as-of date, horizon weeks, minimum cash threshold, stress delay, and refresh timestamp.
2. **Receipts** — Power Query output from customer invoices.
3. **Payments** — Power Query output from supplier and other payments.
4. **Base Forecast** — weekly receipts, payments, net cash flow, opening cash, closing cash, and alert.
5. **Stress Forecast** — the same calculations with delayed unpaid customer receipts.
6. **Scenario Comparison** — base closing cash, stress closing cash, and cash gap by week.
7. **Data Quality** — missing IDs, invalid dates, duplicate IDs, and negative-value checks.

Use conditional formatting for `ALERT`, freeze header rows, and format all monetary values as INR.
