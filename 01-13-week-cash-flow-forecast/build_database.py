from pathlib import Path
import csv
import sqlite3
from datetime import date, timedelta


ROOT = Path(__file__).resolve().parent
RAW = ROOT / "data" / "raw"
DB_PATH = ROOT / "database" / "cash_forecast.sqlite"
OUT = ROOT / "outputs"


def read_csv(name):
    with (RAW / name).open(newline="", encoding="utf-8-sig") as file:
        return list(csv.DictReader(file))


def as_float(value):
    return float(value) if value else None


def load_table(connection, table, rows):
    if not rows:
        return
    columns = list(rows[0])
    placeholders = ",".join("?" for _ in columns)
    connection.executemany(
        f"INSERT INTO {table} ({','.join(columns)}) VALUES ({placeholders})",
        [[as_float(row[column]) if column in {"amount", "opening_cash"} else (row[column] or None) for column in columns] for row in rows],
    )


def week_start(value):
    current = date.fromisoformat(value)
    return current - timedelta(days=current.weekday())


def main():
    DB_PATH.parent.mkdir(exist_ok=True)
    OUT.mkdir(exist_ok=True)
    if DB_PATH.exists():
        DB_PATH.unlink()
    schema = (ROOT / "sql" / "schema_and_views.sql").read_text(encoding="utf-8")
    connection = sqlite3.connect(DB_PATH)
    connection.executescript(schema)
    config = read_csv("forecast_config.csv")
    connection.executemany("INSERT INTO forecast_config VALUES (?, ?)", [(row["config_key"], row["config_value"]) for row in config])
    load_table(connection, "opening_cash", read_csv("opening_cash.csv"))
    load_table(connection, "customer_invoices", read_csv("customer_invoices.csv"))
    load_table(connection, "supplier_payments", read_csv("supplier_payments.csv"))
    load_table(connection, "other_cash_flows", read_csv("other_cash_flows.csv"))
    connection.commit()

    settings = dict(connection.execute("SELECT config_key, config_value FROM forecast_config"))
    start = date.fromisoformat(settings["as_of_date"])
    weeks = [start + timedelta(days=7 * index) for index in range(int(settings["horizon_weeks"]))]
    opening = float(connection.execute("SELECT opening_cash FROM opening_cash").fetchone()[0])
    events = connection.execute("SELECT event_date, amount, flow_type, scenario FROM v_base_cash_events").fetchall()
    stress_events = connection.execute("SELECT event_date, amount, flow_type, scenario FROM v_stress_cash_events").fetchall()

    def build_rows(source_events, scenario):
        nonlocal opening
        rows = []
        closing = opening
        threshold = float(settings["minimum_cash_threshold"])
        for week in weeks:
            end = week + timedelta(days=6)
            receipts = sum(amount for event_date, amount, flow_type, _ in source_events if week <= date.fromisoformat(event_date) <= end and flow_type == "Receipt")
            payments = sum(amount for event_date, amount, flow_type, _ in source_events if week <= date.fromisoformat(event_date) <= end and flow_type == "Payment")
            week_opening = closing
            closing = week_opening + receipts - payments
            rows.append([scenario, week.isoformat(), week_opening, receipts, payments, closing, "ALERT" if closing < threshold else "OK"])
        return rows

    base_rows = build_rows(events, "Base")
    stress_rows = build_rows(stress_events, "Customer_Payments_20_Days_Late")
    with (OUT / "forecast_results.csv").open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["scenario", "week_start", "opening_cash", "receipts", "payments", "closing_cash", "minimum_cash_alert"])
        writer.writerows(base_rows + stress_rows)
    with (OUT / "validation_summary.txt").open("w", encoding="utf-8") as file:
        file.write(f"Database: {DB_PATH.name}\nBase weeks: {len(base_rows)}\nStress weeks: {len(stress_rows)}\n")
        file.write(f"Base minimum cash: {min(row[5] for row in base_rows):.2f}\nStress minimum cash: {min(row[5] for row in stress_rows):.2f}\n")
    connection.close()
    print(f"Created {DB_PATH} and forecast outputs.")


if __name__ == "__main__":
    main()
