# Excel Workbook Blueprint

Create `working_capital_analyzer.xlsx` with these sheets:

1. **Control Panel** — reporting date, period days, DSO improvement days, and refresh timestamp.
2. **AR Aging** — invoice-level open balances, days past due, and aging buckets.
3. **Customer Risk** — risk score, risk band, overdue balance, credit utilization, and cash release.
4. **AP Aging** — open supplier balances, due status, and vendor concentration.
5. **Working Capital KPIs** — DSO, DPO, inventory days, open AR, open AP, and total cash-release opportunity.
6. **DSO Cash Release** — customer-level and top-five cash-release opportunities.
7. **Data Quality** — duplicate IDs, missing master-data keys, invalid dates, and unmatched payments.

Load the SQLite analytical views or Power Query outputs into the workbook and format all monetary values as INR.
