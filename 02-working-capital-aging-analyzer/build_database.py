from pathlib import Path
import csv
import sqlite3


ROOT = Path(__file__).resolve().parent
RAW = ROOT / "data" / "raw"
DB_PATH = ROOT / "database" / "working_capital.sqlite"
OUT = ROOT / "outputs"


TABLE_FILES = {
    "reporting_dates": "reporting_dates.csv",
    "customers": "customers.csv",
    "vendors": "vendors.csv",
    "sales_invoices": "sales_invoices.csv",
    "customer_payments": "customer_payments.csv",
    "purchase_bills": "purchase_bills.csv",
    "supplier_payments": "supplier_payments.csv",
    "inventory_snapshots": "inventory_snapshots.csv",
    "monthly_financials": "monthly_financials.csv",
}


def read_csv(filename):
    with (RAW / filename).open(newline="", encoding="utf-8-sig") as file:
        return list(csv.DictReader(file))


def load_table(connection, table, rows):
    columns = list(rows[0])
    numeric = {"credit_limit", "invoice_amount", "payment_amount", "bill_amount", "inventory_value", "credit_sales", "cogs", "days_in_period", "dso_improvement_days", "payment_terms_days"}
    placeholders = ",".join("?" for _ in columns)
    values = []
    for row in rows:
        values.append([float(row[column]) if column in numeric and "." in row[column] else int(row[column]) if column in numeric else row[column] for column in columns])
    connection.executemany(f"INSERT INTO {table} ({','.join(columns)}) VALUES ({placeholders})", values)


def export_query(connection, query_name, path):
    cursor = connection.execute(f"SELECT * FROM {query_name}")
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([column[0] for column in cursor.description])
        writer.writerows(cursor.fetchall())


def main():
    DB_PATH.parent.mkdir(exist_ok=True)
    OUT.mkdir(exist_ok=True)
    if DB_PATH.exists():
        DB_PATH.unlink()
    connection = sqlite3.connect(DB_PATH)
    connection.executescript((ROOT / "sql" / "schema.sql").read_text(encoding="utf-8"))
    for table, filename in TABLE_FILES.items():
        load_table(connection, table, read_csv(filename))
    connection.executescript((ROOT / "sql" / "aging_analysis.sql").read_text(encoding="utf-8"))
    connection.executescript((ROOT / "sql" / "kpi_analysis.sql").read_text(encoding="utf-8"))
    connection.commit()
    export_query(connection, "ar_aging", OUT / "ar_aging.csv")
    export_query(connection, "customer_risk", OUT / "customer_risk.csv")
    export_query(connection, "ap_open_items", OUT / "ap_open_items.csv")
    export_query(connection, "working_capital_kpis", OUT / "working_capital_kpis.csv")
    connection.close()
    print(f"Created {DB_PATH} and analytical outputs.")


if __name__ == "__main__":
    main()
