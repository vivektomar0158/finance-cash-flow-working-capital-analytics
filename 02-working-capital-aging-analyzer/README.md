# Working Capital and Receivables Aging Analyzer

Standalone working-capital project for the same fictional Indian distribution company. It identifies customers and vendors locking up cash, calculates DSO/DPO/inventory days, and estimates cash released from a five-day DSO improvement.

## Stack

- SQLite for data storage and analytical SQL
- Excel for supporting analysis
- Power BI Desktop for dashboards
- Power Query for refreshable CSV ingestion
- Python only for local SQLite database creation and validation

## Start

```powershell
python build_database.py
python build_workbook.py
```

This creates `database/working_capital.sqlite`, `excel/working_capital_analyzer.xlsx`, and analytical result files in `outputs/`.

## Dashboard questions

- Which customers have the largest overdue balances?
- Which risk bands should collections prioritize?
- What are DSO, DPO, and inventory days?
- How much cash could be released if DSO falls by five days?
- Which vendors represent the largest open-payables concentration?
