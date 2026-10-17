# 13-Week Cash Flow Forecast

Standalone liquidity planning project for a fictional Indian distribution company. It forecasts receipts, payments, and closing cash for 13 weeks and compares a base case with a 20-day customer-payment-delay scenario.

![13-Week Cash Flow Dashboard](powerbi/screenshot/Screenshot%202026-10-17%20092903.png)

## Stack

- SQLite for source and analytical tables
- Excel for the finance model
- Power Query for folder-based refresh
- Power BI Desktop for the dashboard
- Python only for local SQLite database creation and validation

## Start

```powershell
python build_database.py
python build_workbook.py
```

This creates `database/cash_forecast.sqlite`, `excel/13_week_cash_forecast.xlsx`, and validation results in `outputs/`.

## Dashboard questions

- Does closing cash fall below ₹1,000,000 during the 13-week horizon?
- Which weeks have the largest receipts or payment pressure?
- How much cash is lost under the 20-day late-payment scenario?
- What is the first week requiring management action?

## Refresh workflow

Drop new CSV files with the documented columns into `data/raw/`, refresh Power Query in Excel, and refresh the Power BI model. The SQL views use the configured as-of date and minimum cash threshold.
