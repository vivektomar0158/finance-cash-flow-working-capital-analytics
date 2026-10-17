# Power BI Dashboard Build Guide

## Pages

1. **Working Capital Overview:** DSO, DPO, inventory days, open AR, open AP, and cash-release opportunity.
2. **Receivables Aging:** aging buckets, open AR by customer, overdue percentage, and customer drill-through.
3. **Customer Risk and Actions:** risk score, risk band, overdue amount, credit utilization, and DSO cash release.
4. **Vendor and Payables Analysis:** AP aging, vendor balances, due versus overdue payments, and vendor concentration.

## SQLite views

Load `working_capital_kpis`, `ar_aging`, `customer_risk`, and `ap_open_items` from the SQLite database. Use customer and vendor dimensions for drill-through pages.

Recommended measures:

```DAX
Cash Release Opportunity = SUM(CustomerRisk[cash_released_if_dso_improves])
Overdue AR = CALCULATE(SUM(ARAging[open_balance]), ARAging[days_past_due] > 0)
```
