import sqlite3
import csv
import os

# PATHS

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DB_PATH = os.path.join(BASE_DIR, "data", "meesho_reseller.db")
OUTPUT_DIR = os.path.join(BASE_DIR, "part1_sql", "output")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# DATABASE CONNECTION

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# HELPER FUNCTION

def save_query_to_csv(query, output_file):
    cursor.execute(query)

    rows = cursor.fetchall()
    columns = [description[0] for description in cursor.description]

    output_path = os.path.join(OUTPUT_DIR, output_file)

    with open(output_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow(columns)
        writer.writerows(rows)

    #print(f"Created: {output_file}")

# QUESTION 1
# Monthly revenue by category

monthly_category_revenue_query = """
SELECT
    month,
    category,
    ROUND(SUM(quantity * unit_price), 2) AS revenue,
    COUNT(*) AS n_orders
FROM orders
GROUP BY month, category
ORDER BY
    CASE month
        WHEN 'April' THEN 1
        WHEN 'May' THEN 2
        WHEN 'June' THEN 3
    END;
"""

save_query_to_csv(
    monthly_category_revenue_query,
    "monthly_category_revenue(ques1).csv"
)

# QUESTION 2
# Region-wise total revenue and order count

region_revenue_query = """
SELECT
    r.region,
    ROUND(SUM(o.quantity * o.unit_price), 2) AS revenue,
    COUNT(*) AS no_of_orders
FROM orders o
JOIN resellers r
    ON o.reseller_id = r.reseller_id
GROUP BY r.region

UNION ALL

SELECT
    'Grand Total' AS region,
    ROUND(SUM(quantity * unit_price), 2) AS revenue,
    COUNT(*) AS no_of_orders
FROM orders;
"""


save_query_to_csv(
    region_revenue_query,
    "region_revenue(ques2).csv"
)

# QUESTION 3
# Top resellers by total spend

top_resellers_query = """
SELECT
    r.reseller_id,
    r.reseller_name,
    r.region,
    ROUND(SUM(o.quantity * o.unit_price), 2) AS total_spend
FROM orders o
JOIN resellers r
    ON o.reseller_id = r.reseller_id
GROUP BY
    r.reseller_id,
    r.reseller_name,
    r.region
HAVING total_spend > 50000
ORDER BY total_spend DESC
LIMIT 5;
"""

save_query_to_csv(
    top_resellers_query,
    "top_resellers(ques3).csv"
)

# QUESTION 4
# Resellers who have never placed an order

zero_order_query = """
SELECT
    r.reseller_id,
    r.reseller_name,
    r.region
FROM resellers r
LEFT JOIN orders o
    ON r.reseller_id = o.reseller_id
WHERE o.order_id IS NULL
ORDER BY r.reseller_id;
"""

save_query_to_csv(
    zero_order_query,
    "zero_order_resellers(ques4.1).csv"
)


# QUESTION 4 - COUNT(*) vs COUNT(order_id)

zero_order_count_demo_query = """
SELECT
    r.reseller_id,
    r.reseller_name,
    COUNT(*) AS total_rows,
    COUNT(o.order_id) AS matched_orders
FROM resellers r
LEFT JOIN orders o
    ON r.reseller_id = o.reseller_id
WHERE r.reseller_id = 'RS024'
GROUP BY
    r.reseller_id,
    r.reseller_name;
"""

save_query_to_csv(
    zero_order_count_demo_query,
    "zero_order_count_demo(ques4.2).csv"
)

# QUESTION 5
# Average Order Value (AOV) for June, Delivered orders only

june_aov_query = """
SELECT
    ROUND(
        SUM(quantity * unit_price) / COUNT(*),
        2
    ) AS june_delivered_aov
FROM orders
WHERE month = 'June'
  AND status = 'Delivered';
"""

save_query_to_csv(
    june_aov_query,
    "june_aov(ques5).csv"
)



# CLOSE DATABASE


conn.close()

