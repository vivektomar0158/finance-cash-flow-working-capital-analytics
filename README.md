# Finance Analytics Portfolio

Two independent finance analytics projects for a fictional Indian distribution company.

## Projects

- [13-Week Cash Flow Forecast](01-13-week-cash-flow-forecast/README.md): 13-week base forecast, minimum-cash alert, and 20-day late-payment stress scenario.
- [Working Capital and Aging Analyzer](02-working-capital-aging-analyzer/README.md): AR/AP aging, DSO, DPO, inventory days, customer risk, and DSO cash-release analysis.

## Technology

SQLite, SQL, Excel, Power Query, Power BI Desktop, and Python for local reproducible database/output generation.

## Run the local data builds

```powershell
python 01-13-week-cash-flow-forecast/build_database.py
python 01-13-week-cash-flow-forecast/build_workbook.py
python 02-working-capital-aging-analyzer/build_database.py
python 02-working-capital-aging-analyzer/build_workbook.py
```

The generated Excel workbooks are stored in each project's `excel` folder. Power BI `.pbix` files must be created with Power BI Desktop using the documented output files and dashboard guides.

The `powerbi` folders include the downloaded PBIX files and dashboard screenshots as reference assets. The included SQL, synthetic data, Excel workbooks, and Power BI guides document the original project implementation.

## Data note

All included data is synthetic and safe for public portfolio use.
