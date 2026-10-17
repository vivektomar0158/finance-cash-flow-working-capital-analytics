DROP VIEW IF EXISTS customer_risk;
CREATE VIEW customer_risk AS
WITH customer_ar AS (
    SELECT customer_id,
        SUM(open_balance) AS open_ar,
        SUM(CASE WHEN days_past_due > 0 THEN open_balance ELSE 0 END) AS overdue_ar,
        MAX(CASE WHEN days_past_due > 0 THEN days_past_due ELSE 0 END) AS oldest_overdue_days
    FROM ar_aging
    GROUP BY customer_id
), scored AS (
    SELECT customer.*, customer_ar.open_ar, customer_ar.overdue_ar, customer_ar.oldest_overdue_days,
        customer_ar.open_ar / customer.credit_limit AS credit_utilization,
        customer_ar.overdue_ar / customer_ar.open_ar AS overdue_pct,
        customer_ar.open_ar / (SELECT SUM(open_ar) FROM customer_ar) AS concentration_pct
    FROM customers customer JOIN customer_ar USING (customer_id)
), scored_with_risk AS (
    SELECT *,
        ROUND(MIN(overdue_pct * 40 + MIN(oldest_overdue_days, 90) / 90.0 * 25 + credit_utilization * 20 + concentration_pct * 15, 100), 1) AS risk_score,
        ROUND(
            (open_ar / SUM(open_ar) OVER ()) *
            (SELECT credit_sales * dso_improvement_days / days_in_period
             FROM monthly_financials CROSS JOIN reporting_dates LIMIT 1),
            2
        ) AS cash_released_if_dso_improves
    FROM scored
)
SELECT *,
    CASE
        WHEN risk_score >= 70 THEN 'High'
        WHEN risk_score >= 40 THEN 'Medium'
        ELSE 'Low'
    END AS risk_band
FROM scored_with_risk;

DROP VIEW IF EXISTS working_capital_kpis;
CREATE VIEW working_capital_kpis AS
SELECT
    (SELECT reporting_date FROM reporting_dates LIMIT 1) AS reporting_date,
    (SELECT SUM(open_balance) FROM ar_open_items) AS open_ar,
    (SELECT SUM(open_balance) FROM ap_open_items) AS open_ap,
    (SELECT inventory_value FROM inventory_snapshots ORDER BY snapshot_date DESC LIMIT 1) AS inventory_value,
    (SELECT SUM(open_balance) FROM ar_open_items) / (SELECT credit_sales / days_in_period FROM monthly_financials CROSS JOIN reporting_dates LIMIT 1) AS dso_estimate_days,
    (SELECT SUM(open_balance) FROM ap_open_items) / (SELECT cogs / days_in_period FROM monthly_financials CROSS JOIN reporting_dates LIMIT 1) AS dpo_estimate_days,
    (SELECT inventory_value FROM inventory_snapshots ORDER BY snapshot_date DESC LIMIT 1) / (SELECT cogs / days_in_period FROM monthly_financials CROSS JOIN reporting_dates LIMIT 1) AS inventory_days,
    (SELECT credit_sales * dso_improvement_days / days_in_period
     FROM monthly_financials CROSS JOIN reporting_dates LIMIT 1) AS cash_release_opportunity;
