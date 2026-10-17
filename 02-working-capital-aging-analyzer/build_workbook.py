from pathlib import Path
import csv

from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "outputs"
RAW = ROOT / "data" / "raw"
WORKBOOK = ROOT / "excel" / "working_capital_analyzer.xlsx"
BLUE = "1F4E78"


def read_csv(filename):
    with (OUTPUT / filename).open(newline="", encoding="utf-8-sig") as file:
        return list(csv.DictReader(file))


def write_table(sheet, rows, table_name):
    if not rows:
        return
    headers = list(rows[0])
    sheet.append(headers)
    for row in rows:
        sheet.append([row[column] for column in headers])
    last_row = sheet.max_row
    table = Table(displayName=table_name, ref=f"A1:{get_column_letter(sheet.max_column)}{last_row}")
    table.tableStyleInfo = TableStyleInfo(name="TableStyleMedium2", showRowStripes=True, showColumnStripes=False)
    sheet.add_table(table)
    sheet.freeze_panes = "A2"


def style_sheet(sheet):
    for cell in sheet[1]:
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor=BLUE)
        cell.alignment = Alignment(horizontal="center")
    for column_cells in sheet.columns:
        width = min(max(len(str(cell.value or "")) for cell in column_cells) + 2, 30)
        sheet.column_dimensions[get_column_letter(column_cells[0].column)].width = width


def main():
    aging = read_csv("ar_aging.csv")
    risk = read_csv("customer_risk.csv")
    ap = read_csv("ap_open_items.csv")
    kpis = read_csv("working_capital_kpis.csv")
    workbook = Workbook()
    control = workbook.active
    control.title = "Control Panel"
    control.append(["Working Capital Analyzer", "Value"])
    for key, value in [("Company", "Pragati Distribution Pvt Ltd"), ("Currency", "INR"), ("Reporting Date", kpis[0]["reporting_date"]), ("DSO Improvement Assumption", "5 days"), ("Period Length", "30 days")]:
        control.append([key, value])
    control["A8"] = "Refresh instructions"
    control["A8"].font = Font(bold=True, color="FFFFFF")
    control["A8"].fill = PatternFill("solid", fgColor=BLUE)
    control["A9"] = "Rebuild the SQLite database after replacing raw files, then refresh the workbook queries."
    control.merge_cells("A9:B9")

    for name, dataset, table_name in [("AR Aging", aging, "ARAging"), ("Customer Risk", risk, "CustomerRisk"), ("AP Aging", ap, "APAging")]:
        sheet = workbook.create_sheet(name)
        write_table(sheet, dataset, table_name)
        style_sheet(sheet)
    raw_sources = [
        ("Raw Customers", "customers.csv", "RawCustomers"),
        ("Raw Vendors", "vendors.csv", "RawVendors"),
        ("Raw Sales Invoices", "sales_invoices.csv", "RawSalesInvoices"),
        ("Raw Customer Payments", "customer_payments.csv", "RawCustomerPayments"),
        ("Raw Purchase Bills", "purchase_bills.csv", "RawPurchaseBills"),
        ("Raw Supplier Payments", "supplier_payments.csv", "RawSupplierPayments"),
        ("Raw Inventory", "inventory_snapshots.csv", "RawInventory"),
        ("Raw Monthly Financials", "monthly_financials.csv", "RawMonthlyFinancials"),
        ("Raw Reporting Dates", "reporting_dates.csv", "RawReportingDates"),
    ]
    for name, filename, table_name in raw_sources:
        sheet = workbook.create_sheet(name)
        write_table(sheet, read_csv(RAW / filename), table_name)
        style_sheet(sheet)
    kpi_sheet = workbook.create_sheet("Working Capital KPIs")
    write_table(kpi_sheet, kpis, "WorkingCapitalKPIs")
    style_sheet(kpi_sheet)
    release = workbook.create_sheet("DSO Cash Release")
    release_rows = [{"customer_id": row["customer_id"], "customer_name": row["customer_name"], "open_ar": row["open_ar"], "cash_released_if_dso_improves": row["cash_released_if_dso_improves"]} for row in risk]
    write_table(release, release_rows, "DSOCashRelease")
    style_sheet(release)
    chart = BarChart()
    chart.title = "Cash Release Opportunity by Customer"
    chart.y_axis.title = "INR"
    chart.add_data(Reference(release, min_col=4, min_row=1, max_row=release.max_row), titles_from_data=True)
    chart.set_categories(Reference(release, min_col=2, min_row=2, max_row=release.max_row))
    release.add_chart(chart, "F2")
    quality = workbook.create_sheet("Data Quality")
    quality.append(["Check", "Result"])
    quality.append(["AR rows loaded", len(aging)])
    quality.append(["Customer risk rows loaded", len(risk)])
    quality.append(["AP rows loaded", len(ap)])
    quality.append(["AR balances reconcile", "PASS" if round(sum(float(row["open_balance"]) for row in aging), 2) == round(sum(float(row["open_ar"]) for row in risk), 2) else "FAIL"])
    quality.append(["KPI output loaded", "PASS" if kpis else "FAIL"])
    style_sheet(quality)
    for sheet in workbook.worksheets:
        sheet.sheet_view.showGridLines = False
        for row in sheet.iter_rows():
            for cell in row:
                if isinstance(cell.value, (int, float)):
                    cell.number_format = '#,##0.00'
    WORKBOOK.parent.mkdir(exist_ok=True)
    try:
        workbook.save(WORKBOOK)
        saved_path = WORKBOOK
    except PermissionError:
        saved_path = WORKBOOK.with_name("working_capital_analyzer_with_raw_data.xlsx")
        workbook.save(saved_path)
    print(f"Created {saved_path}")


if __name__ == "__main__":
    main()
